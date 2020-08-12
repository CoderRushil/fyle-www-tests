import time
import logging
import pytest

from common.asserts import assert_overflowing, assert_customer_testimonial, assert_customer_logo, assert_cta_click_and_modal_show
from common.test_getdemo import assert_bad_email, assert_missing_firstname, assert_success
from common.download_feature_list_form import assert_bad_email_download_feature_form, assert_missing_firstname_download_feature_form, assert_success_download_feature_form
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + "/expense-management")
    return module_browser

# check demo form (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    assert_bad_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    assert_missing_firstname(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    assert_success(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_feature_scroll(browser):
    browser.click(xpath="//section[@class='feature-hero']//a[text()='Expense Reporting']")
    time.sleep(2)
    e = browser.find(xpath="//section[@id='expense-reporting']")
    assert abs(e.location['y'] - browser.current_scroll_position()) <= 30, 'Not scrolling to the Expense Reporting feature'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_collpasing_section(browser):
    for i in range(1, 11):
        time.sleep(2)
        browser.find(xpath=f"//a[@id='feature-{i}']/ancestor::section", scroll=True)
        section = browser.click(xpath=f"//a[@id='feature-{i}']")
        class_list = section.get_attribute('class')
        assert class_list.count('collapse-closed collapsed'), 'Collapsing of sections should work'

# check download feature list form
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email_download_feature_form(browser):
    assert_bad_email_download_feature_form(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname_download_feature_form(browser):
    assert_missing_firstname_download_feature_form(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success_download_feature_form(browser):
    assert_success_download_feature_form(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_overflowing(browser):
    assert_overflowing(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_customer_testimonial(browser):
    assert_customer_testimonial(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    assert_customer_logo(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_bottom_section_cta(browser):
    cta_section_xpath = '//section[contains(@class, "feature-bottom-section")]'
    cta_xpath = f'{cta_section_xpath}//a'
    assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath)
