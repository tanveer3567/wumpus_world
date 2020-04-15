#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        check_true_false
# Purpose:     Main entry into logic program. Reads input files, creates 
#              base, tests statement, and generates result file.
#
# Created:     09/25/2011
# Last Edited: 07/22/2013     
# Notes:       *Ported by Christopher Conly from C++ code supplied by Dr. 
#               Vassilis Athitsos.
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so I put it in a list, which
#               is passed by reference.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from logical_expression import logical_expression, read_expression, print_expression, valid_expression, check_true_false

def main(argv):
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    # Create the knowledge base with wumpus rules
    print '\nLoading wumpus rules...'
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print 'Loading additional knowledge...'
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.
    print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print 'Loading statement...'
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    
    # Convert statement into a logical expression and verify it is valid
    print (statement)
    negation = '(not ' + statement + ')'
    print (negation)
    statement = read_expression(statement)
    counter = [0]
    negation = read_expression(negation, counter)
    if not valid_expression(statement):
        sys.exit('invalid statement')
    if not valid_expression(negation):
        sys.exit('invalid statement')

    # Show us what the statement is
    print '\nChecking statement: ',
    print
    print_expression(statement, '')
    print
    print_expression(negation, '')
    print
    print
    print ("Does knowledge base entails alpha ?")

    # Run the statement through the inference engine
    entails_alpha, negation_entails_alpha = check_true_false(knowledge_base, statement, negation)

    try:
        outputFile = open('output.txt', 'w')
        output_txt = ""
        if entails_alpha == True and negation_entails_alpha == False:
            output_txt = "definitely true"
        elif entails_alpha == False and negation_entails_alpha == True:
            output_txt = "definitely false"
        elif entails_alpha == False and negation_entails_alpha == False:
            output_txt = "possibly true, possibly false"
        elif entails_alpha == True and negation_entails_alpha == True:
            output_txt = "both true and false"
        else:
            output_txt = "error"
        print (output_txt)
        outputFile.write(output_txt)
        outputFile.close()
    except:
        print('failed to create output file')

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)
