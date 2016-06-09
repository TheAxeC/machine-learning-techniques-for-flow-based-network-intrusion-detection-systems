
experiments = [
    (0.805596692458, 0.830762578285),
    (0.805085467831, 0.830210640663),
    (0.806935614098, 0.831186777151),
    (0.805685953901 ,0.830049639495 ),
    (0.805994311612 ,0.830825653429 ),
    (0.806042999671 ,0.830704034143 ),
    (0.806375701412 ,0.831329370479 ),
    (0.805815788726 ,0.830998233308 ),
    (0.804955633006 ,0.831152345488 ),
    (0.805332965468 ,0.830129376312 )
]

to_calculate = "cross"

def calculate_ctu(recall, precision):
    total = 195519
    actual_pos = 708.9 + 56182.1

    true_pos = recall * actual_pos
    false_pos = true_pos / precision - true_pos
    false_neg = actual_pos - true_pos
    true_neg = total - true_pos - false_pos - false_neg

    return total, true_pos, true_neg, false_neg, false_pos


def calculate_cross(recall, precision):
    total = 246467
    actual_pos = 107839

    true_pos = recall * actual_pos
    false_pos = true_pos / precision - true_pos
    false_neg = actual_pos - true_pos
    true_neg = total - true_pos - false_pos - false_neg

    return total, true_pos, true_neg, false_neg, false_pos

def do_calcs():
    func = calculate_ctu
    if to_calculate == "cross":
        func = calculate_cross

    tab = {}
    tab['tp'] = []
    tab['tn'] = []
    tab['fp'] = []
    tab['fn'] = []
    avg = {}
    var = {}

    total = 0
    for e in experiments:
        a, b, c, d, e = func(e[0], e[1])
        total = a

        tab['tp'].append(b)
        tab['tn'].append(c)
        tab['fn'].append(d)
        tab['fp'].append(e)

        s = ""
        s += 'Total amount of samples & ' + str(a) + " \\\\" + "\n"
        s += 'False negative & ' + str(d) + " \\\\" + "\n"
        s += 'False positive & ' + str(e) + " \\\\" + "\n"
        s += 'True negative & ' + str(c) + " \\\\" + "\n"
        s += 'True positive & ' + str(b) + " \\\\" + "\n"
        print s
        print ""

    for key, value in tab.iteritems():
        val = 0.0
        for item in value:
            val += item
        try:
            avg[key] = val / len(value)
        except ZeroDivisionError:
            avg[key] = -1

        val = 0.0
        for item in value:
            val += (avg[key] - item) ** 2
        try:
            var[key] = val / len(value)
        except ZeroDivisionError:
            var[key] = -1

    s = "Average\n"
    s += 'Total amount of samples & ' + str(total) + " \\\\" + "\n"
    s += 'False negative & ' + str(avg['fn']) + " \\\\" + "\n"
    s += 'False positive & ' + str(avg['fp']) + " \\\\" + "\n"
    s += 'True negative & ' + str(avg['tn']) + " \\\\" + "\n"
    s += 'True positive & ' + str(avg['tp']) + " \\\\" + "\n"
    print s
    print ""

    s = "Variance\n"
    s += 'Total amount of samples & ' + str(total) + " \\\\" + "\n"
    s += 'False negative & ' + str(var['fn']) + " \\\\" + "\n"
    s += 'False positive & ' + str(var['fp']) + " \\\\" + "\n"
    s += 'True negative & ' + str(var['tn']) + " \\\\" + "\n"
    s += 'True positive & ' + str(var['tp']) + " \\\\" + "\n"
    print s
    print ""

if __name__ == "__main__":
    do_calcs()
