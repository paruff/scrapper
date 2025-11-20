Feature: VRM Scraper acceptance criteria
  As a researcher
  I want the scraper to parse VRM pages, respect safety limits,
  and write Excel outputs with stable headers
  So that I can analyze listings reliably.

  Scenario: Extract inline JSON model into properties
    Given sample VRM HTML with two properties
    When I extract the inline model
    Then the result has 2 properties
    And the first property has name "Beach House Paradise" and city "Virginia Beach"

  Scenario: Respect per-state page cap and avoid extra follows
    Given a spider configured with max pages 1 for state "VA"
    When I parse a page containing a next link for that state
    Then no follow request is produced

  Scenario: Write Excel with per-state sheet and ordered headers
    Given an open Excel pipeline in a temporary directory
    When I process an item for state "VA" with fields in a specific order
    Then the workbook has a sheet "VA" with headers matching the item key order