
# A logging class
class Logger:

    def __init__(self):
        pass

    # Start the log file
    def start(self, dest):
        import os
        if not os.path.exists(os.path.dirname(dest)):
            try:
                os.makedirs(os.path.dirname(dest))
            except OSError as exc: # Guard against race condition
                pass
        try:
            self.logger = open(dest, 'w')
        except IOError as e:
            print "Could not open file: \"" + dest + "\"."

    # Output that a malicious packet has been found
    def output_malicious(self, label, flow):
        self.logger.write("Malicious label found \"" + str(label) + "\"!!!!!!!!!!!\n")
        self.output(flow)
        self.logger.flush()

    # Output a good label
    def output_good(self, label):
        self.logger.write("Good label found \"" + label + "\"\n")
        self.logger.flush()

    # Output whether a label is good or bad
    def output_complete(self, label, flow, good_labels):
        if label in good_labels:
            self.output_good(label)
        else:
            self.output_malicious(label, flow)

    # Standard output for a flow packet
    def output(self, flow):
        self.logger.write("\t protocol: " + str(flow.protocol) + "\n")
        self.logger.write("\t address: from: " + str(flow.src_ip) + " to " + str(flow.dest_ip) + "\n")
        self.logger.write("\t ports: from: " + str(flow.src_port) + " to " + str(flow.dest_port) + "\n")
        self.logger.write("\t packets: " + str(flow.total_pckts) + " with " + str(flow.total_bytes) + " bytes\n")
        self.logger.write("\t duration: " + str(flow.duration) + " starting from " + str(flow.start_time) + "\n")
        self.logger.flush()

    def output_check(self, label, flow, correct):
        self.logger.write("Uncorrect labeling: \n")
        self.logger.write("\t got " + str(label) + " expected: " + str(correct) + "\n")
        self.output(flow)


    # Close the log file
    def close(self):
        if self.logger:
            self.logger.close()
            self.logger = None

    def write(self, str):
        self.logger.write(str)
        self.logger.flush()

    # update_progress() : Displays or updates a console progress bar
    ## Accepts a float between 0 and 1. Any int will be converted to a float.
    ## A value under 0 represents a 'halt'.
    ## A value at 1 or bigger represents 100%
    # src: http://stackoverflow.com/questions/3160699/python-progress-bar
    def update_progress(self, progress):
        import time, sys
        barLength = 50 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        sys.stdout.write(text)
        sys.stdout.flush()
