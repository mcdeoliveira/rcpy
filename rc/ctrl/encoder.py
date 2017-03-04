if __name__ == "__main__":

    import sys
    sys.path.append('.')
    sys.path.append('/root/beaglebone/python')

import ctrl.block as block

import rc.encoder as encdr

class Encoder(block.BufferBlock):
        
    def __init__(self,
                 ratio = 48 * 172, 
                 encoder = 2,
                 *vars, **kwargs):

        # gear ratio
        self.ratio = ratio

        # encoder
        self.encoder = encoder

        # call super
        super().__init__(*vars, **kwargs)
        
        # output is in cycles
        self.buffer = (encdr.read(self.encoder) / self.ratio, )

    def set(self, **kwargs):
        
        if 'ratio' in kwargs:
            self.ratio = kwargs.pop('ratio')

        super().set(**kwargs)

    def reset(self):

        encdr.set(self.encoder, 0)

    def write(self, *values):

        encdr.set(self.encoder, int(values[0] * self.ratio))

    def read(self):

        #print('> read')
        if self.enabled:

            self.buffer = (encdr.read(self.encoder) / self.ratio, )
        
        return self.buffer


if __name__ == "__main__":

    import time, math
    from time import perf_counter
    import itertools

    T = 0.04
    K = 1000

    print("\n> Testing Encoder")

    e1 = Encoder(encoder = 1)
    e2 = Encoder(encoder = 2)
    e3 = Encoder(encoder = 3)
    e4 = Encoder(encoder = 4)
    
    print('\n ENC #1 |  ENC #2 |  ENC #3 |  ENC #4')
    
    N = 10
    for k in range(N):

        print('\r{:7.3f} | {:7.3f} | {:7.3f} | {:7.3f}'.format(*itertools.chain(e1.read(),
                                                                       e2.read(),
                                                                       e3.read(),
                                                                       e4.read())),
              end='')

        time.sleep(1)
                
