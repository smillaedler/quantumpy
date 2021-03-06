#!/usr/bin/env python
# encoding: utf-8

from cmath import exp, pi, sqrt
from random import random


class Psi:
    def __init__(self, n_qubits):
        """
        set up a quantum system with the given number of qubits
        initialized to the "zero" qubit.
        """
        self.n_qubits = n_qubits
        # in this classical simulation, we use 2^n_qubits complex numbers
        self.amplitudes = [0] * (1 << n_qubits)
        self.amplitudes[0] = 1
    
    def collapse(self):
        """
        collapse the system (i.e. measure it) and return a tuple
        of the bits.
        """
        weights = [abs(amp) ** 2 for amp in self.amplitudes]
        choice = random() * sum(weights)
        for i, w in enumerate(weights):
            choice -= w
            if choice < 0:
                self.amplitudes = [0] * (1 << self.n_qubits)
                self.amplitudes[i] = 1
                return tuple((i >> bit) % 2 for bit in range(self.n_qubits))
    
    ## gates
    
    def pi_over_eight(self, qubit):
        """
        applies a π/8 gate to the given qubit
        """
        # has to be a valid qubit
        if qubit > self.n_qubits:
            raise ValueError()
        # go through each amplitude
        for i in range(1 << self.n_qubits):
            # find out whether that amplitude corresponds to the qubit being
            # zero or one
            if (i >> qubit) % 2 == 0:  # if zero
                self.amplitudes[i] *= exp(-1j * pi / 8)
            else:  # if one
                self.amplitudes[i] *= exp(1j * pi / 8)

    def controlled_not(self, qubit1, qubit2):
        """
        applies a controlled-not gate using the first given qubit as the
        control of the permutation of the second.
        """
        # the two quibits have to valid and different
        if qubit1 > self.n_qubits or qubit2 > self.n_qubits or qubit1 == qubit2:
            raise ValueError()
        # make a copy of amplitudes as they update simultaneously
        old_amplitudes = self.amplitudes[:]
        # go through each amplitude
        for i in range(1 << self.n_qubits):
            # permutate qubit2 based on value of qubit1
            self.amplitudes[i ^ (((i >> qubit1) % 2) << qubit2)] = old_amplitudes[i]

    def hadamard(self, qubit):
        """
        applies a Hadamard gate to the given qubit.
        """
        # has to be a valid qubit
        if qubit > self.n_qubits:
            raise ValueError()
        # make a copy of amplitudes as they update simultaneously
        old_amplitudes = self.amplitudes[:]
        # go through each amplitude
        for i in range(1 << self.n_qubits):
            # find out whether that amplitude corresponds to the qubit being
            # zero or one
            if (i >> qubit) % 2 == 0:  # if zero
                self.amplitudes[i] = (old_amplitudes[i] - old_amplitudes[i + (1 << qubit)]) / sqrt(2)
            else:  # if one
                self.amplitudes[i] = (old_amplitudes[i - (1 << qubit)] - old_amplitudes[i]) / sqrt(2)


if __name__ == "__main__":
    
    # set up a system with 3 qubits
    psi = Psi(3)
    
    # apply Hadamard gate to qubit 1 (second qubit)
    psi.hadamard(1)
    # apply Hadamard gate to qubit 2 (third qubit)
    psi.hadamard(2)
    # apply π/8 gate to qubit 1
    psi.pi_over_eight(1)
    # apply controlled-not gate with qubit 1 controlling qubit 0 (first qubit)
    psi.controlled_not(1, 0)
    
    # collapse and print the result (a tuple of 3 classical bits)
    print(psi.collapse())
