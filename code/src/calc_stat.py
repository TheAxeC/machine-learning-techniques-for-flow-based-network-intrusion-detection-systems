
recall = [
0.993286287892,
0.993239922477,
0.994955442836,
0.993193557062,
0.993230649394,
0.993221376311,
0.993601572715,
0.993620118881,
0.993536661134,
0.993675757379
]

precision = [
0.950165435143,
0.951032186459,
0.951382361808,
0.950827385391,
0.95002793965 ,
0.949597936042,
0.950990050679,
0.950602826498,
0.950716973096,
0.950841637311
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

def calculate_class(recall, precision):
    total = 226467
    actual_pos = 13077 + 74762

    true_pos = recall * actual_pos
    false_pos = true_pos / precision - true_pos
    false_neg = actual_pos - true_pos
    true_neg = total - true_pos - false_pos - false_neg
    return total, true_pos, true_neg, false_neg, false_pos

def do_calcs():
    func = calculate_ctu
    if to_calculate == "cross":
        func = calculate_cross
    elif to_calculate == "class":
        func = calculate_class

    tab = {}
    tab['tp'] = []
    tab['tn'] = []
    tab['fp'] = []
    tab['fn'] = []
    avg = {}
    var = {}

    total = 0
    i = 0
    while i < 10:
        a, b, c, d, e = func(recall[i], precision[i])
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
        i += 1

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
    s += 'Total amount of samples & ' + str(0) + " \\\\" + "\n"
    s += 'False negative & ' + str(var['fn']) + " \\\\" + "\n"
    s += 'False positive & ' + str(var['fp']) + " \\\\" + "\n"
    s += 'True negative & ' + str(var['tn']) + " \\\\" + "\n"
    s += 'True positive & ' + str(var['tp']) + " \\\\" + "\n"
    print s
    print ""

if __name__ == "__main__":
    do_calcs()
