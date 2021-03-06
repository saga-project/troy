

import os
import saga

import radical.utils as ru

from   troy.constants import *
import troy


# ------------------------------------------------------------------------------
#
PLUGIN_DESCRIPTION = {
    'type'        : 'workload_dispatcher', 
    'name'        : 'local', 
    'version'     : '0.1',
    'description' : 'this is a simple dispatcher which forks CUs locally.'
  }


# ------------------------------------------------------------------------------
#
class PLUGIN_CLASS (troy.PluginBase):
    """
    This plugin creates compute units via fork/exec.  It is not a clever plugin.

    **Configuration Options:** None
    """

    __metaclass__ = ru.Singleton


    # --------------------------------------------------------------------------
    #
    def __init__ (self) :

        troy.PluginBase.__init__ (self, PLUGIN_DESCRIPTION)

        # cache saga dirs for file staging
        self._dir_cache = dict()


    # --------------------------------------------------------------------------
    #
    def dispatch (self, workload, overlay) :
        """
        dig the commands out of the unit descriptions, and run them as
        subprocesses.
        """

        for tid in workload.tasks.keys () :

            task = workload.tasks[tid]

            for unit_id in task['units'] :
                unit     = task['units'][unit_id]

                if  not unit.staged_in and task.as_dict ()['inputs'] :
                    raise RuntimeError ("cannot dispatch %s - stage-in not done" % unit.id)

                unit_descr     = unit.as_dict ()

              # print "----------------------------------"
              # print unit_descr
              # print "----------------------------------"

                pid            = unit.pilot_id
                pilot          = troy.Pilot (overlay.session, pid)
                pilot_instance = pilot._get_instance ('default')
                unit_instance  = pilot_instance.submit_unit (unit_descr)
                troy._logger.info ('workload dispatch : dispatch %-23s to %s' % (unit_id, pid))

                unit._set_instance ('default', self, unit_instance, unit_instance.id)


    # --------------------------------------------------------------------------
    #
    def unit_get_info (self, unit) :
        """
        Check the state of the subprocesses
        """

        # find out what we can about the pilot...
        u = unit._get_instance ('default')

        info = dict()

        # hahaha python switch statement hahahahaha
        info['state'] =  {"New"      : DISPATCHED, 
                          "Running"  : RUNNING, 
                          "Failed"   : FAILED, 
                          "Done"     : DONE, 
                          "Canceled" : CANCELED}.get (u.state, UNKNOWN)

        info['slots']            = 1
        info['start_time']       = u.start
        info['agent_start_time'] = -1
        info['job_id']           = u.id 
        info['end_queue_time']   = -1 

        return info


    # --------------------------------------------------------------------------
    #
    def unit_cancel (self, unit) :
        """
        Kill the sub processes
        """

        u = unit._get_instance ('default')
        u.cancel ()


# ------------------------------------------------------------------------------

