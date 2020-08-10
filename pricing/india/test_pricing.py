import logging
import time
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

# base url; read about @pytest.fixture
@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/pricing")
    module_browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"India"}')
    module_browser.refresh()
    time.sleep(5)
    return module_browser

# check customer logo section (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert indian_logo.is_displayed() and not us_logo.is_displayed(), 'Found an US image in Indian IP'

# check pricing page is redirecting to bcp page
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bcp_redirection(browser):
    browser.click(xpath="//a[contains(text(), 'Click here')]")
    bcp_h1 = browser.find(xpath="//h1")
    assert 'Business continuity at Fyle:' in bcp_h1.text, 'Redirection to bcp failed'

# check all 3 pricing cards have cta which open demo form
@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_cards_cta(browser):
    card_ctas = browser.find_many("//div[contains(@class, 'card-footer')]")
    close_form = browser.find("//button[contains(@class, 'close')]")
    for cta in card_ctas:
        cta.click()
        time.sleep(3)
        close_form.click()
        time.sleep(3)

# check pricing: Indian prices should be shown
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_pricing_text(browser):
    browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"India"}')
    browser.refresh()
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h1[contains(@class, 'business-price')]")
    assert standard_price.text == 'Custom pricing' and business_price.text == 'Custom pricing', 'Pricing is incorrect for India'
    standard_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-outline-primary') and contains(text(), 'Contact us')]")
    business_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-primary') and contains(text(), 'Contact us')]")
    assert standard_card_cta and business_card_cta, 'Pricing cards cta text is wrong'

# check toggle of compare plans table
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_compareplan_table(browser):
    table = browser.find(xpath="//div[contains(@class, 'feature-table')]")
    assert table and table.is_displayed() is False, 'Compare all plans table is already open, by default'
    browser.force_click(xpath="//button[contains(text(), 'Compare all plans')]")
    assert table and table.is_displayed(), 'Compare all plans table is not opening'

# check the ctas present inside the compare all plans table
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_download_cta(browser):
    time.sleep(3)
    browser.force_click(xpath="//button[contains(text(), 'Compare all plans')]")
    browser.force_click(xpath="//button[contains(text(), 'Download all plans')]")
    time.sleep(3)
    download_form = browser.find(xpath="//form[@id='contact-us-form-feature-download']")
    assert download_form and download_form.is_displayed(), 'All feature download form is not open'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_demo_cta(browser):
    time.sleep(3)
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    browser.click(xpath="//div[contains(@class, 'compare-all-cta')]//button[contains(text(), 'Get a demo')]")
    demo_form = browser.find(xpath="//form[@id='contact-us-form']")
    assert demo_form and demo_form.is_displayed(), 'Demo form is not open'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_scroll_top(browser):
    time.sleep(3)
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    browser.scroll_down(100)
    time.sleep(3)
    browser.click(xpath="//a[contains(@class, 'scroll-top-arrow')]")
    time.sleep(3)
    business_pricing_card = browser.find(xpath="//h2[contains(@class, 'card-title') and contains(text(), 'Business')]")
    assert business_pricing_card.is_displayed(), 'Scroll top is not scrolling to the desired section'

# check FAQ collapsibles
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_collapsible_faq(browser):
    faq_answer = browser.find(xpath="//div[@id='faq-1-content']")
    assert faq_answer.is_displayed() is False, 'FAQ answer is not collapsed by default'
    browser.click(xpath="//div[@id='faq-1-heading']")
    assert faq_answer.is_displayed(), 'FAQ answer is not opening on click'
    browser.click(xpath="//div[@id='faq-1-heading']")
    time.sleep(2)
    assert faq_answer.is_displayed() is False, 'FAQ answer is not collapsing on click'

# check table header for compare all plans is sticky or not
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_sticky_table_header(browser):
    browser.scroll_into_view(xpath="//div[contains(@class, 'table-data') and contains(text(), 'Real-time Policy Violations')]")
    header_position = browser.get_computed_style(xpath="//div[contains(@class, 'table-head')]", key="position")
    assert header_position == 'sticky', 'Compare all plans table header is not sticky'

# check collapsible pricing card details in mobile
@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_collapsible_details(browser):
    browser.force_click(xpath="//a[@id='show-hide-standard']")
    time.sleep(3)
    details_display = browser.find(xpath="//a[@id='standard-collapse']", scroll=True)
    assert details_display and details_display.is_displayed(), 'Show details is not opening the collapsible'