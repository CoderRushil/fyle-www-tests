import time
import logging
import pytest
from common.utils import resize_browser
from common.chrome_uninstall_form import assert_required_fields, assert_invalid_email, assert_success_chrome_uninstall_form

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + '/chrome-uninstall')
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_required_fields(browser):
    assert_required_fields(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_invalid_email(browser):
    assert_invalid_email(browser)

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_non_business_email(browser):
#     assert_non_business_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success_chrome_uninstall_form(browser):
    assert_success_chrome_uninstall_form(browser)
    