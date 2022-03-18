package co.com.appgate.swordphish.runners;

import cucumber.api.CucumberOptions;
import cucumber.api.SnippetType;
import net.serenitybdd.cucumber.CucumberWithSerenity;
import org.junit.runner.RunWith;

@RunWith(CucumberWithSerenity.class)
@CucumberOptions(features = "src/test/resources/validate_url.feature",
        glue = "co.com.appgate.swordphish.stepdefinitions",
        snippets = SnippetType.CAMELCASE)
public class ValidateUrl {
}
