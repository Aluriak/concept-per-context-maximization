
import sys
import time
import scoring


class Propagator:
    def init(self, init):
        self.__init = init
        self.__sleep = .1
        self.__symbols = {atom.literal for atom in init.symbolic_atoms}
        for atom in init.symbolic_atoms:
            # print('STPLTE:', atom)
            # print('      :', atom.literal)
            # print('      :', atom.symbol)
            # print('      :', atom.is_fact)
            # print('      :', atom.is_external)
            init.add_watch(init.solver_literal(atom.literal))
        print('LITERALS:', self.__symbols)

    def propagate(self, ctl, changes):
        # print('BLAQIȦ:', ctl)
        # help(ctl)
        for l in changes:
            # print('.', end='', flush=True)
            # time.sleep(self.__sleep)
            pass
        return True

    def undo(self, solver_id, assign, undo):
        # scoring.reset()
        for l in undo:
            # print("\b \b", end='', flush=True)
            # time.sleep(self.__sleep)
            pass

    def check(self, ctl):
        # print('CHECKING…')
        # print(ctl, ctl.assignment.size)
        # print(ctl.assignment)
        # print(dir(ctl))
        # print(dir(ctl.assignment))
        for lit in self.__symbols:
            # print(lit, ctl.assignment.is_fixed(lit), ctl.assignment.value(lit), ctl.assignment.has_literal(lit), ctl.assignment.level(lit))
            # print(lit, ctl.assignment.has_literal(lit))
            # print(lit, ctl.assignment.is_fixed(lit))
            # print(lit, ctl.assignment.value(lit))
            # print(lit, ctl.assignment.level(lit))
            pass
        # return False


def main(prg):
    prg.register_propagator(Propagator())
    prg.ground([("base", [])])
    prg.solve()
    print()
