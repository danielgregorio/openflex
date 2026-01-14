// Tree-sitter Grammar for ActionScript 4 (OpenFlex Neo)
// This grammar defines the syntax for AS4 including modern features

module.exports = grammar({
  name: 'actionscript4',

  extras: $ => [
    /\s/,
    $.comment,
  ],

  word: $ => $.identifier,

  conflicts: $ => [
    [$.block, $.object_literal],
    [$.parameter, $.expression],
    [$.type, $.generic_type],
    [$.await_expression, $.call_expression],
    [$.arrow_function, $.call_expression],
    [$.arrow_function, $.ternary_expression],
    [$.nullable_type, $.union_type],
    [$.nullable_type, $.function_type],
    [$.union_type, $.function_type],
    [$.union_type],
    [$.match_expression, $.match_statement],
    [$.if_statement],
  ],

  rules: {
    // Entry point
    source_file: $ => repeat($._statement),

    // Comments
    comment: $ => choice(
      seq('//', /.*/),
      seq('/*', /[^*]*\*+([^/*][^*]*\*+)*/, '/')
    ),

    // Statements
    _statement: $ => choice(
      $.import_statement,
      seq($.variable_declaration, ';'),  // Add semicolon at call site
      $.function_declaration,
      $.class_declaration,
      $.interface_declaration,
      $.trait_declaration,
      $.type_alias,
      $.conditional_compilation_block,
      $.expression_statement,
      $.if_statement,
      $.for_statement,
      $.for_in_statement,
      $.for_of_statement,
      $.while_statement,
      $.return_statement,
      $.break_statement,
      $.continue_statement,
      $.throw_statement,
      $.try_statement,
      $.match_statement,
      $.block,
    ),

    // Import statements (AS3-style)
    import_statement: $ => seq(
      'import',
      $.import_path,
      optional(seq('as', $.identifier)),
      ';'
    ),

    import_path: $ => seq(
      $.identifier,
      repeat(seq('.', choice($.identifier, '*')))
    ),

    // Variable declarations with decorators (no semicolon - added at call sites)
    variable_declaration: $ => seq(
      optional($.decorator_list),
      optional($.visibility),
      optional('static'),
      choice('var', 'const'),
      field('name', $.identifier),
      optional(seq(':', field('type', $.type))),
      optional(seq('=', field('value', $.expression)))
    ),

    // Function declarations with decorators
    function_declaration: $ => seq(
      optional(field('decorators', $.decorator_list)),
      optional(field('visibility', $.visibility)),
      optional('static'),
      optional('async'),
      'function',
      field('name', $.identifier),
      field('parameters', $.parameter_list),
      optional(seq(':', field('return_type', $.type))),
      field('body', $.block)
    ),

    // Class declarations
    class_declaration: $ => seq(
      optional($.visibility),
      'class',
      $.identifier,
      optional($.type_parameters),
      optional(seq('extends', $.type)),
      optional(seq('implements', commaSep1($.type))),
      $.class_body
    ),

    class_body: $ => seq(
      '{',
      repeat(choice(
        $.method_declaration,            // Methods (no 'function' keyword)
        $.constructor_declaration,
        seq($.property_declaration, ';')  // Properties
      )),
      '}'
    ),

    // Method declaration for class members (no 'function' keyword)
    method_declaration: $ => seq(
      optional(field('decorators', $.decorator_list)),
      optional(field('visibility', $.visibility)),
      optional('static'),
      optional('async'),
      field('name', $.identifier),
      field('parameters', $.parameter_list),
      optional(seq(':', field('return_type', $.type))),
      field('body', $.block)
    ),

    // Property declaration for class members (no var/const keyword)
    property_declaration: $ => seq(
      optional($.decorator_list),
      optional($.visibility),
      optional('static'),
      field('name', $.identifier),
      optional(seq(':', field('type', $.type))),
      optional(seq('=', field('value', $.expression)))
    ),

    constructor_declaration: $ => seq(
      optional($.visibility),
      'constructor',
      $.parameter_list,
      $.block
    ),

    // Interface declarations
    interface_declaration: $ => seq(
      'interface',
      $.identifier,
      optional($.type_parameters),
      optional(seq('extends', commaSep1($.type))),
      $.interface_body
    ),

    interface_body: $ => seq(
      '{',
      repeat($.interface_member),
      '}'
    ),

    interface_member: $ => seq(
      $.identifier,
      optional(seq(':', $.type)),
      ';'
    ),

    // Trait declarations (AS4 extension)
    trait_declaration: $ => seq(
      'trait',
      $.identifier,
      optional($.type_parameters),
      $.trait_body
    ),

    trait_body: $ => seq(
      '{',
      repeat(choice(
        $.function_declaration,
        seq($.variable_declaration, ';')  // Add semicolon at call site
      )),
      '}'
    ),

    // Type alias
    type_alias: $ => seq(
      'type',
      $.identifier,
      optional($.type_parameters),
      '=',
      $.type,
      ';'
    ),

    // Decorators (for @reactive, @computed, @effect)
    decorator_list: $ => repeat1($.decorator),

    decorator: $ => seq(
      '@',
      $.identifier,
      optional($.argument_list)
    ),

    // Conditional compilation
    conditional_compilation_block: $ => seq(
      '#if',
      $.condition_expression,
      repeat($._statement),
      repeat(seq(
        '#elif',
        $.condition_expression,
        repeat($._statement)
      )),
      optional(seq(
        '#else',
        repeat($._statement)
      )),
      '#endif'
    ),

    condition_expression: $ => choice(
      $.identifier,  // WEB, MOBILE, etc.
      seq('!', $.condition_expression),
      seq('(', $.condition_expression, ')'),
      prec.left(2, seq($.condition_expression, '&&', $.condition_expression)),
      prec.left(1, seq($.condition_expression, '||', $.condition_expression)),
    ),

    // Types
    type: $ => choice(
      $.identifier,
      $.nullable_type,
      $.union_type,
      $.array_type,
      $.generic_type,
      $.function_type,
    ),

    nullable_type: $ => seq($.type, '?'),

    union_type: $ => prec.left(seq(
      $.type,
      repeat1(seq('|', $.type))
    )),

    array_type: $ => seq('Array', '<', $.type, '>'),

    generic_type: $ => seq(
      $.identifier,
      '<',
      commaSep1($.type),
      '>'
    ),

    function_type: $ => seq(
      '(',
      optional(commaSep1($.type)),
      ')',
      '=>',
      $.type
    ),

    type_parameters: $ => seq(
      '<',
      commaSep1($.type_parameter),
      '>'
    ),

    type_parameter: $ => seq(
      $.identifier,
      optional(seq('extends', $.type))
    ),

    // Parameters
    parameter_list: $ => seq(
      '(',
      optional(commaSep1($.parameter)),
      ')'
    ),

    parameter: $ => seq(
      optional('...'),
      $.identifier,
      optional(seq(':', $.type)),
      optional(seq('=', $.expression))
    ),

    // Expressions
    expression: $ => choice(
      $.identifier,
      $.literal,
      $.binary_expression,
      $.unary_expression,
      $.call_expression,
      $.member_expression,
      $.new_expression,
      $.array_literal,
      $.object_literal,
      $.arrow_function,
      $.await_expression,
      $.ternary_expression,
      $.match_expression,
      $.parenthesized_expression,
    ),

    literal: $ => choice(
      $.number,
      $.string,
      $.boolean,
      $.null
    ),

    number: $ => /\d+(\.\d+)?/,
    string: $ => choice(
      seq('"', /[^"]*/, '"'),
      seq("'", /[^']*/, "'"),
      $.template_string
    ),
    boolean: $ => choice('true', 'false'),
    null: $ => 'null',

    template_string: $ => seq(
      '`',
      repeat(choice(
        /[^`$]/,
        seq('${', $.expression, '}')
      )),
      '`'
    ),

    binary_expression: $ => choice(
      prec.left(10, seq($.expression, '*', $.expression)),
      prec.left(10, seq($.expression, '/', $.expression)),
      prec.left(9, seq($.expression, '+', $.expression)),
      prec.left(9, seq($.expression, '-', $.expression)),
      prec.left(7, seq($.expression, '<', $.expression)),
      prec.left(7, seq($.expression, '>', $.expression)),
      prec.left(7, seq($.expression, '<=', $.expression)),
      prec.left(7, seq($.expression, '>=', $.expression)),
      prec.left(6, seq($.expression, '==', $.expression)),
      prec.left(6, seq($.expression, '!=', $.expression)),
      prec.left(4, seq($.expression, '??', $.expression)),  // Nullish coalescing
      prec.left(3, seq($.expression, '&&', $.expression)),
      prec.left(2, seq($.expression, '||', $.expression)),
      prec.right(1, seq($.expression, '=', $.expression)),
    ),

    unary_expression: $ => prec.left(13, choice(
      seq('-', $.expression),
      seq('!', $.expression),
      seq('++', $.expression),
      seq('--', $.expression),
      seq($.expression, '++'),
      seq($.expression, '--'),
    )),

    call_expression: $ => seq(
      $.expression,
      $.argument_list
    ),

    argument_list: $ => seq(
      '(',
      optional(commaSep1($.expression)),
      ')'
    ),

    member_expression: $ => prec.left(16, choice(
      seq($.expression, '.', $.identifier),
      seq($.expression, '[', $.expression, ']'),
      seq($.expression, '?.', $.identifier),  // Optional chaining
    )),

    new_expression: $ => seq(
      'new',
      $.type,
      $.argument_list
    ),

    array_literal: $ => seq(
      '[',
      optional(commaSep1(choice(
        $.expression,
        $.spread_element  // Allow spread in arrays
      ))),
      ']'
    ),

    object_literal: $ => seq(
      '{',
      optional(commaSep1(choice(
        $.property,
        $.spread_element  // Allow spread in objects
      ))),
      '}'
    ),

    property: $ => seq(
      choice(
        $.identifier,
        $.string,
        seq('[', $.expression, ']')
      ),
      ':',
      $.expression
    ),

    spread_element: $ => seq(
      '...',
      $.expression
    ),

    arrow_function: $ => seq(
      choice(
        $.identifier,
        $.parameter_list
      ),
      '=>',
      choice(
        $.expression,
        $.block
      )
    ),

    await_expression: $ => prec.right(12, seq(
      'await',
      $.expression
    )),

    ternary_expression: $ => prec.right(seq(
      $.expression,
      '?',
      $.expression,
      ':',
      $.expression
    )),

    parenthesized_expression: $ => seq(
      '(',
      $.expression,
      ')'
    ),

    // Match expression (pattern matching)
    match_expression: $ => seq(
      'match',
      $.expression,
      '{',
      repeat1($.match_case),
      '}'
    ),

    match_statement: $ => seq(
      'match',
      $.expression,
      '{',
      repeat1($.match_case),
      '}'
    ),

    match_case: $ => seq(
      $.pattern,
      '=>',
      choice($.expression, $.block),
      optional(',')
    ),

    pattern: $ => choice(
      $.identifier,
      $.literal,
      seq($.identifier, '(', optional(commaSep1($.pattern)), ')'),
      seq('[', optional(commaSep1($.pattern)), ']'),
      seq('{', optional(commaSep1($.property_pattern)), '}'),
      '_',  // Wildcard
    ),

    property_pattern: $ => seq(
      $.identifier,
      optional(seq(':', $.pattern))
    ),

    // Control flow statements
    if_statement: $ => seq(
      'if',
      '(',
      $.expression,
      ')',
      $._statement,
      optional(seq('else', $._statement))
    ),

    for_statement: $ => seq(
      'for',
      '(',
      optional(choice(
        $.variable_declaration,  // No semicolon - it's part of for syntax
        $.expression
      )),
      ';',
      optional($.expression),
      ';',
      optional($.expression),
      ')',
      $._statement
    ),

    for_in_statement: $ => seq(
      'for',
      '(',
      choice($.variable_declaration, $.identifier),
      'in',
      $.expression,
      ')',
      $._statement
    ),

    for_of_statement: $ => seq(
      'for',
      '(',
      choice($.variable_declaration, $.identifier),
      'of',
      $.expression,
      ')',
      $._statement
    ),

    while_statement: $ => seq(
      'while',
      '(',
      $.expression,
      ')',
      $._statement
    ),

    return_statement: $ => seq(
      'return',
      optional($.expression),
      ';'
    ),

    break_statement: $ => seq('break', ';'),
    continue_statement: $ => seq('continue', ';'),

    throw_statement: $ => seq(
      'throw',
      $.expression,
      ';'
    ),

    try_statement: $ => seq(
      'try',
      $.block,
      optional($.catch_clause),
      optional(seq('finally', $.block))
    ),

    catch_clause: $ => seq(
      'catch',
      '(',
      $.identifier,
      optional(seq(':', $.type)),
      ')',
      $.block
    ),

    expression_statement: $ => seq($.expression, ';'),

    block: $ => seq(
      '{',
      repeat($._statement),
      '}'
    ),

    // Visibility modifiers
    visibility: $ => choice('public', 'private', 'protected'),

    // Identifier
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
  }
});

// Helper function for comma-separated lists
function commaSep1(rule) {
  return seq(rule, repeat(seq(',', rule)));
}
