Feature: Economic Growth Areas
  As a residential real estate investor
  I want a list of economically growing areas
  So that I can find properties in those areas

  Scenario: Request growth areas for Virginia
    Given a state "VA"
    When the user requests growth areas
    Then the system provides a list of economically growing areas
    And the list includes "Northern Virginia"
    And the list includes growth indicators

  Scenario: Request growth areas for Texas
    Given a state "TX"
    When the user requests growth areas
    Then the system provides a list of economically growing areas
    And the list includes "Austin Metro"

  Scenario: Request growth areas for unsupported state
    Given a state "ZZ"
    When the user requests growth areas
    Then the system returns an empty list

  Scenario: Get all supported states
    When the user requests all supported states
    Then the list includes "VA"
    And the list includes "TX"
    And the list includes "NC"
    And the list includes "FL"
    And the list includes "CA"
