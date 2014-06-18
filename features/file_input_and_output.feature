Feature: Using a dutch file as input and other file as an output
  In order to tokenize the file
  Using a file as an input
  Using a file as an output

  Scenario Outline: tokenize dutch input file.
    Given the kaf file "<kaf_file>"
    And I put them through the kernel
    Then the output should match the fixture "<output_file>"
  Examples:
    | kaf_file  | output_file |
    | input-de.kaf | output-de.kaf  |
    | input-en.kaf | output-en.kaf  |
    | input-es.kaf | output-es.kaf  |
    | input-fr.kaf | output-fr.kaf  |
    | input-it.kaf | output-it.kaf  |
    | input-nl.kaf | output-nl.kaf  |

