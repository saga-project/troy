

import radical.utils as ru

from   troy.constants import *
import troy


# ------------------------------------------------------------------------------
#
PLUGIN_DESCRIPTION = {
    'type'        : 'workload_translator', 
    'name'        : 'direct', 
    'version'     : '0.1',
    'description' : 'this is a sime translator which defines one CU per task.'
  }


# ------------------------------------------------------------------------------
#
class PLUGIN_CLASS (troy.PluginBase) :
    """
    This is a simple workload translator, which will create exactly one CU per
    task.  This is not a clever plugin.
    """

    __metaclass__ = ru.Singleton
    
    
    # --------------------------------------------------------------------------
    #
    def __init__ (self) :

        troy.PluginBase.__init__ (self, PLUGIN_DESCRIPTION)


    # --------------------------------------------------------------------------
    #
    def translate (self, workload, overlay=None) :
        """
        Iterate over tasks, and essentially cast the task's description into
        a CU description.  Et voila!
        """

        for tid in workload.tasks.keys () :

            task = workload.tasks[tid]

            # we simply and stupidly translate one task into one unit description
            cu_descr = troy.ComputeUnitDescription (task.as_dict ())
            cu_id    = task._add_unit (cu_descr)
            troy._logger.info ('workload translate: derive unit %-18s for %s' % (cu_id, task.id))


# ------------------------------------------------------------------------------

