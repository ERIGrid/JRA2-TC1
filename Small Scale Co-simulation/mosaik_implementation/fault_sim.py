'''This is a simple module that can serve as a mosaik simulator to allow users
to provide input to another simulator that introduces a fault into that system.'''
import itertools
import mosaik_api

meta = {
    'models': {
        'Fault': {
            'public': True,
            'attrs': ['output'],
            'params': ['rp',    # Input that is provided before the fault event
            'postrp',           # Input that is provided after the fault event
            'time_thresh']      # Time of the fault event
        }
    }
}

class FaultSim(mosaik_api.Simulator):
    '''The module follows the standard mosaik interface structure.'''
    def __init__(self):
        super(FaultSim, self).__init__(meta)
        self.sid = None

        self.cache = None
        self._entities = {}
        self.eid_counters = {}
        self._entities = {}

    def init(self, sid, step_size=1, time_factor=0.01):
        self.sid = sid
        self.step_size = step_size
        self.time_factor = time_factor

        return self.meta

    def create(self, num, model, **model_params):
        counter = self.eid_counters.setdefault(model, itertools.count())

        entities = []

        for i in range(num):
            eid = '%s_%s' % (model, next(counter))

            self._entities[eid] = model_params

            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs=None):
        self.cache = {}
        actual_time = t * self.time_factor
        for eid, mod in self._entities.items():
            # Check if event time has been reached and choose output accordingly:
            if actual_time < mod['time_thresh']:
                self.cache[eid] = mod['rp']
            else:
                self.cache[eid] = mod['postrp']

        return t + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.cache[eid]

        return data
