#Author: Santiago Gomez Bedoya

Feature: As a use I want to validate URL with swordphish service

  @primero
  Scenario Outline: URL Success
    When the user send to url
      | <urls> | <phishing> |
    And the information
      | correlationId   | traceabilityId   | replyTo   |
      | <correlationId> | <traceabilityId> | <replyTo> |
    Then the user will see a score with criteria of 0.5

    Examples:
      | correlationId | traceabilityId | urls                      | replyTo                                  | phishing |
      | 027           | PRUEBA027      | https://www.google.com    | dtp.weblogs-service.1.reply.analyze-urls | false    |
      | 028           | PRUEBA028      | https://www.apple.com     | dtp.weblogs-service.1.reply.analyze-urls | false    |
      | 029           | PRUEBA029      | https://www.bonbonite.com | dtp.weblogs-service.1.reply.analyze-urls | false    |
      | 030           | PRUEBA030      | https://www.falabella.com | dtp.weblogs-service.1.reply.analyze-urls | false    |


  Scenario: Page Phishing
    When the user send to url
      | http://facbok.com | true |
    And the information
      | correlationId | traceabilityId | replyTo        |
      | 031           | PRUEBA031      | TestSwordphish |
    Then the user will see a score with criteria of 0.5

  @phisingylegal
  Scenario: Legal page and phishing page
    When the user send to url
      | http://www.futurama.com                              | false |
      | http://comtudoparavoce.online/oferts/acompanhamento/ | true  |
    And the information
      | correlationId | traceabilityId | replyTo                                  |
      | 031           | prueba031      | dtp.weblogs-service.1.reply.analyze-urls |
    Then the user will see a score with criteria of 0.5

  Scenario: Legal pages
    When the user send to url
      | http://www.dubal.com/                                                            | false |
      | http://kreditmini.ru/category/potrebitelskie-kredity/?yclid/=3288921934936704012 | false |
      | http://200.10.171.43/sodimac-cl/CMR-puntos                                       | false |
    And the information
      | correlationId | traceabilityId | replyTo                                  |
      | 032           | prueba032      | dtp.weblogs-service.1.reply.analyze-urls |
    Then the user will see a score with criteria of 0.5

  @pagelegal
  Scenario: Phishing pages
    When the user send to url
      | http://smbcracojp.com                   | true |
      | http://l3ancofalabellacl.com/falalogin/ | true |
    And the information
      | correlationId | traceabilityId | replyTo                                  |
      | 032           | prueba032      | dtp.weblogs-service.1.reply.analyze-urls |
    Then the user will see a score with criteria of 0.5
