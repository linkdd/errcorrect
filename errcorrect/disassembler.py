# -*- coding: utf-8 -*-

import dis


def disassemble(co, lasti=-1):
    """
    Disassemble a code object.

    :param co: code object
    :type: code

    :param lasti: last instruction executed (optional)
    :type lasti: int

    :returns: disassembled code
    :rtype: dict
    """

    result = []

    code = co.co_code
    labels = dis.findlabels(code)
    linestarts = dict(dis.findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None

    while i < n:
        instruction = {}

        c = code[i]
        op = ord(c)

        if i in linestarts:
            instruction['linestarts'] = linestarts[i]

        instruction['lasti'] = (i == lasti)
        instruction['labelled'] = (i in labels)
        instruction['i'] = i
        instruction['opname'] = dis.opname[op]

        i += 1

        if op >= dis.HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
            extended_arg = 0
            i += 2

            if op == dis.EXTENDED_ARG:
                extended_arg = oparg * 65536

            instruction['oparg'] = {
                'count': oparg
            }

            if op in dis.hasconst:
                instruction['oparg']['type'] = 'consts'
                instruction['oparg']['val'] = co.co_consts[oparg]

            elif op in dis.hasname:
                instruction['oparg']['type'] = 'names'
                instruction['oparg']['val'] = co.co_names[oparg]

            elif op in dis.hasjrel:
                instruction['oparg']['type'] = 'jump'
                instruction['oparg']['val'] = i + oparg

            elif op in dis.haslocal:
                instruction['oparg']['type'] = 'varnames'
                instruction['oparg']['val'] = co.co_varnames[oparg]

            elif op in dis.hascompare:
                instruction['oparg']['type'] = 'compare'
                instruction['oparg']['val'] = dis.cmp_op[oparg]

            elif op in dis.hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars

                instruction['oparg']['type'] = 'free'
                instruction['oparg']['val'] = free[oparg]

        result.append(instruction)

    return result
