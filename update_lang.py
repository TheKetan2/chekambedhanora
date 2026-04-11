import re
import os

filepath = r"c:\Users\Ketan\Downloads\Work\gram panchayat websites\chekambedhanora\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

def replacer(match):
    mr, en = match.groups()
    return f'<span class="lang-mr">{mr.strip()}</span><span class="lang-en">{en.strip()}</span>'

# Replace specific strings.

replacements = [
    # Top info
    ('<p class="text-sm font-semibold text-primary-base">ग्रामपंचायत चेक आंबेधानोरा</p>', '<p class="text-sm font-semibold text-primary-base"><span class="lang-mr">ग्रामपंचायत चेक आंबेधानोरा</span><span class="lang-en">Gram Panchayat Chek Ambedhanora</span></p>'),
    ('<p class="text-xs text-slate-500">Gram Panchayat Chek Ambedhanora</p>', ''),
    
    # Desktop Nav
    ('<span class="hidden lg:inline">मुख्यपृष्ठ / </span>Home', '<span class="lang-mr">मुख्यपृष्ठ</span><span class="lang-en">Home</span>'),
    ('<span class="hidden lg:inline">माहिती / </span>About', '<span class="lang-mr">माहिती</span><span class="lang-en">About</span>'),
    ('<span class="hidden lg:inline">सदस्य / </span>Members', '<span class="lang-mr">सदस्य</span><span class="lang-en">Members</span>'),
    ('<span class="hidden lg:inline">गॅलरी / </span>Gallery', '<span class="lang-mr">गॅलरी</span><span class="lang-en">Gallery</span>'),
    ('<span class="hidden lg:inline">योजना / </span>Schemes', '<span class="lang-mr">योजना</span><span class="lang-en">Schemes</span>'),
    ('<span class="hidden lg:inline">चौकशी / </span>Query', '<span class="lang-mr">चौकशी</span><span class="lang-en">Query</span>'),
    ('<span class="hidden lg:inline">संपर्क / </span>Contact', '<span class="lang-mr">संपर्क</span><span class="lang-en">Contact</span>'),
    
    # Mobile Nav
    ('<span class="font-medium">मुख्यपृष्ठ / Home</span>', '<span class="font-medium"><span class="lang-mr">मुख्यपृष्ठ</span><span class="lang-en">Home</span></span>'),
    ('<span class="font-medium">माहिती / About</span>', '<span class="font-medium"><span class="lang-mr">माहिती</span><span class="lang-en">About</span></span>'),
    ('<span class="font-medium">सदस्य / Members</span>', '<span class="font-medium"><span class="lang-mr">सदस्य</span><span class="lang-en">Members</span></span>'),
    ('<span class="font-medium">गॅलरी / Gallery</span>', '<span class="font-medium"><span class="lang-mr">गॅलरी</span><span class="lang-en">Gallery</span></span>'),
    ('<span class="font-medium">योजना / Schemes</span>', '<span class="font-medium"><span class="lang-mr">योजना</span><span class="lang-en">Schemes</span></span>'),
    ('<span class="font-medium">चौकशी / Query</span>', '<span class="font-medium"><span class="lang-mr">चौकशी</span><span class="lang-en">Query</span></span>'),
    ('<span class="font-medium">संपर्क / Contact</span>', '<span class="font-medium"><span class="lang-mr">संपर्क</span><span class="lang-en">Contact</span></span>'),

    # Hero
    ('ग्रामपंचायत चेक आंबेधानोरा\n                </h1>', '<span class="lang-mr">ग्रामपंचायत चेक आंबेधानोरा</span><span class="lang-en">Gram Panchayat Chek Ambedhanora</span>\n                </h1>'),
    ('Grampanchayat Chek Ambedhanora \n                </h2>', ''),
    ('पंचायत समिति पोंभुर्णा , जिल्हा चंद्रपूर  | Panchayat Samiti Pombhurna, District Chandrapur', '<span class="lang-mr">पंचायत समिती पोंभुर्णा, जिल्हा चंद्रपूर</span><span class="lang-en">Panchayat Samiti Pombhurna, District Chandrapur</span>'),
    ('"स्वच्छ गाव, समृद्ध गाव" | "Clean Village, Prosperous Village"', '<span class="lang-mr">"स्वच्छ गाव, समृद्ध गाव"</span><span class="lang-en">"Clean Village, Prosperous Village"</span>'),
    ('अधिक जाणून घ्या / Learn More', '<span class="lang-mr">अधिक जाणून घ्या</span><span class="lang-en">Learn More</span>'),

    # About Section
    ('माहिती / About', '<span class="lang-mr">माहिती</span><span class="lang-en">About</span>'),
    ('गावाची ओळख | Village Overview', '<span class="lang-mr">गावाची ओळख</span><span class="lang-en">Village Overview</span>'),
    ('लोकसंख्या / Population', '<span class="lang-mr">लोकसंख्या</span><span class="lang-en">Population</span>'),
    ('क्षेत्रफळ / Area', '<span class="lang-mr">क्षेत्रफळ</span><span class="lang-en">Area</span>'),
    ('कुटुंबे / Households', '<span class="lang-mr">कुटुंबे</span><span class="lang-en">Households</span>'),
    ('संपर्क / Contact', '<span class="lang-mr">संपर्क</span><span class="lang-en">Contact</span>'),

    # Members Section
    ('सदस्य / Members', '<span class="lang-mr">सदस्य</span><span class="lang-en">Members</span>'),
    ('ग्रामपंचायत सदस्य | Panchayat Members', '<span class="lang-mr">ग्रामपंचायत सदस्य</span><span class="lang-en">Panchayat Members</span>'),
    ('<h3 class="text-lg font-semibold text-slate-900 mb-1">सौ निरंजना विकास मडावी</h3>', '<h3 class="text-lg font-semibold text-slate-900 mb-1"><span class="lang-mr">सौ निरंजना विकास मडावी</span><span class="lang-en">Sau Niranjana Vikas Madavi</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-2">Sau Niranjana Vikas Madavi</p>', ''),
    ('प्रशासाक  / Administrator', '<span class="lang-mr">प्रशासक</span><span class="lang-en">Administrator</span>'),
    ('<h3 class="text-lg font-semibold text-slate-900 mb-1">श्री राजेश तुरे </h3>', '<h3 class="text-lg font-semibold text-slate-900 mb-1"><span class="lang-mr">श्री राजेश तुरे</span><span class="lang-en">Shree Rajesh Ture</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-2">Shree Rajesh Ture</p>', ''),
    ('ग्रामपंचायत अधिकारी / Grampanchayat Officer', '<span class="lang-mr">ग्रामविकास अधिकारी</span><span class="lang-en">Gramvikas Officer</span>'),

    # Gallery Section
    ('गॅलरी / Gallery', '<span class="lang-mr">गॅलरी</span><span class="lang-en">Gallery</span>'),
    ('गावाची छायाचित्रे | Village Photos', '<span class="lang-mr">गावाची छायाचित्रे</span><span class="lang-en">Village Photos</span>'),
    ('ग्रामपंचायत चेक आंबेधानोरा / Grampanchayat Chek Ambedhanora</p>', '<span class="lang-mr">ग्रामपंचायत चेक आंबेधानोरा</span><span class="lang-en">Grampanchayat Chek Ambedhanora</span></p>'),
    ('व्यायाम शाळा  / Gym</p>', '<span class="lang-mr">व्यायाम शाळा</span><span class="lang-en">Gym</span></p>'),
    ('अभ्यासिका / Library </p>', '<span class="lang-mr">अभ्यासिका</span><span class="lang-en">Library</span></p>'),
    ('सभा  / Meeting</p>', '<span class="lang-mr">सभा</span><span class="lang-en">Meeting</span></p>'),
    ('स्मशानभूमी  / Smashanbhumi</p>', '<span class="lang-mr">स्मशानभूमी</span><span class="lang-en">Smashanbhumi</span></p>'),
    ('स्वच्छता अभियान   / Swachata Abhiyan</p>', '<span class="lang-mr">स्वच्छता अभियान</span><span class="lang-en">Swachata Abhiyan</span></p>'),
    ('माउली झाकी</p>', '<span class="lang-mr">माउली झाकी</span><span class="lang-en">Mauli Jhaki</span></p>'),
    ('वरिष्ठ अधिकारी भेट</p>', '<span class="lang-mr">वरिष्ठ अधिकारी भेट</span><span class="lang-en">Senior Officer Visit</span></p>'),

    # Info Section
    ('योजना / Schemes', '<span class="lang-mr">योजना</span><span class="lang-en">Schemes</span>'),
    ('सरकारी योजना व सूचना | Government Schemes & Notices', '<span class="lang-mr">सरकारी योजना व सूचना</span><span class="lang-en">Government Schemes & Notices</span>'),
    ('<h3 class="text-lg font-semibold text-slate-900">प्रधानमंत्री आवास योजना</h3>', '<h3 class="text-lg font-semibold text-slate-900"><span class="lang-mr">प्रधानमंत्री आवास योजना</span><span class="lang-en">Pradhan Mantri Awas Yojana</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-1">Pradhan Mantri Awas Yojana</p>', ''),
    ('नवीन / New', '<span class="lang-mr">नवीन</span><span class="lang-en">New</span>'),
    ('घरकुल योजनेसाठी अर्ज करा | Apply for housing scheme', '<span class="lang-mr">घरकुल योजनेसाठी अर्ज करा</span><span class="lang-en">Apply for housing scheme</span>'),
    
    ('<h3 class="text-lg font-semibold text-slate-900">स्वच्छ भारत मिशन</h3>', '<h3 class="text-lg font-semibold text-slate-900"><span class="lang-mr">स्वच्छ भारत मिशन</span><span class="lang-en">Swachh Bharat Mission</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-1">Swachh Bharat Mission</p>', ''),
    ('शौचालय बांधकाम अनुदान | Toilet construction subsidy', '<span class="lang-mr">शौचालय बांधकाम अनुदान</span><span class="lang-en">Toilet construction subsidy</span>'),
    
    ('<h3 class="text-lg font-semibold text-slate-900 mb-1">कृषी सिंचन योजना</h3>', '<h3 class="text-lg font-semibold text-slate-900 mb-1"><span class="lang-mr">कृषी सिंचन योजना</span><span class="lang-en">Krishi Sinchan Yojana</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-1">Krishi Sinchan Yojana</p>', ''),
    ('सूक्ष्म सिंचन सुविधा | Micro irrigation facility', '<span class="lang-mr">सूक्ष्म सिंचन सुविधा</span><span class="lang-en">Micro irrigation facility</span>'),
    
    ('<h3 class="text-lg font-semibold text-slate-900 mb-1">महात्मा गांधी रोजगार हमी</h3>', '<h3 class="text-lg font-semibold text-slate-900 mb-1"><span class="lang-mr">महात्मा गांधी रोजगार हमी</span><span class="lang-en">MGNREGA</span></h3>'),
    ('<p class="text-sm text-slate-500 mb-1">MGNREGA</p>', ''),
    ('रोजगार नोंदणी सुरू | Employment registration open', '<span class="lang-mr">रोजगार नोंदणी सुरू</span><span class="lang-en">Employment registration open</span>'),

    # Contact form
    ('संपर्क करा / Contact Us', '<span class="lang-mr">संपर्क करा</span><span class="lang-en">Contact Us</span>'),
    ('तुमची चौकशी पाठवा | Submit Your Query', '<span class="lang-mr">तुमची चौकशी पाठवा</span><span class="lang-en">Submit Your Query</span>'),
    ('ग्रामपंचायतशी संपर्क साधण्यासाठी खालील फॉर्म भरा | Fill the form below to contact the Gram Panchayat', '<span class="lang-mr">ग्रामपंचायतशी संपर्क साधण्यासाठी खालील फॉर्म भरा</span><span class="lang-en">Fill the form below to contact the Gram Panchayat</span>'),
    
    ('धन्यवाद! / Thank You!', '<span class="lang-mr">धन्यवाद!</span><span class="lang-en">Thank You!</span>'),
    ('तुमची चौकशी यशस्वीरित्या प्राप्त झाली. आम्ही लवकरच संपर्क साधू.<br>\n                                Your query has been submitted successfully. We will contact you soon.', '<span class="lang-mr">तुमची चौकशी यशस्वीरित्या प्राप्त झाली. आम्ही लवकरच संपर्क साधू.</span><span class="lang-en">Your query has been submitted successfully. We will contact you soon.</span>'),
    ('नवीन चौकशी पाठवा / Submit Another Query', '<span class="lang-mr">नवीन चौकशी पाठवा</span><span class="lang-en">Submit Another Query</span>'),
    
    ('नाव / Name', '<span class="lang-mr">नाव</span><span class="lang-en">Name</span>'),
    ('फोन नंबर / Phone', '<span class="lang-mr">फोन नंबर</span><span class="lang-en">Phone</span>'),
    ('ईमेल / Email', '<span class="lang-mr">ईमेल</span><span class="lang-en">Email</span>'),
    ('(ऐच्छिक / Optional)', '<span class="lang-mr">(ऐच्छिक)</span><span class="lang-en">(Optional)</span>'),
    ('चौकशीचा प्रकार / Query Type', '<span class="lang-mr">चौकशीचा प्रकार</span><span class="lang-en">Query Type</span>'),
    ('विषय / Subject', '<span class="lang-mr">विषय</span><span class="lang-en">Subject</span>'),
    ('संदेश / Message', '<span class="lang-mr">संदेश</span><span class="lang-en">Message</span>'),
    ('चौकशी पाठवा / Submit Query', '<span class="lang-mr">चौकशी पाठवा</span><span class="lang-en">Submit Query</span>'),
    ('आवश्यक माहिती / Required fields', '<span class="lang-mr">आवश्यक माहिती</span><span class="lang-en">Required fields</span>'),

    ('ग्रामपंचायत कार्यालय, चेक आंबेधानोरा, ता. पोंभुर्णा, जि. चंद्रपूर - 442905</p>', '<span class="lang-mr">ग्रामपंचायत कार्यालय, चेक आंबेधानोरा, ता. पोंभुर्णा, जि. चंद्रपूर - ४४२९०५</span><span class="lang-en">Gram Panchayat Office, Chek Ambedhanora, Tal. Pombhurna, Dist. Chandrapur - 442905</span></p>'),
    ('<p class="text-white/60 text-sm leading-relaxed">Gram Panchayat Office, Chek Ambedhanora, Tal. Pombhurna, Dist. Chandrapur - 442905</p>', ''),
    ('पत्ता / Address', '<span class="lang-mr">पत्ता</span><span class="lang-en">Address</span>'),
    ('सर्व हक्क राखीव / All Rights Reserved.', '<span class="lang-mr">सर्व हक्क राखीव</span><span class="lang-en">All Rights Reserved.</span>'),
    ('ग्रामपंचायत आंबेधानोरा</h3>', '<span class="lang-mr">ग्रामपंचायत चेक आंबेधानोरा</span><span class="lang-en">Gram Panchayat Chek Ambedhanora</span></h3>'),
    ('<p class="text-white/70 text-sm">Gram Panchayat Ambedhanora</p>', ''),
]

# For form inputs with placeholders, we update them to be handled by JS.
# e.g., <input ... placeholder="तुमचे पूर्ण नाव / Your full name" ...>
# becomes <input ... data-mr-placeholder="तुमचे पूर्ण नाव" data-en-placeholder="Your full name" placeholder="तुमचे पूर्ण नाव" ...>
placeholders = [
    ('placeholder="तुमचे पूर्ण नाव / Your full name"', 'data-mr-placeholder="तुमचे पूर्ण नाव" data-en-placeholder="Your full name" placeholder="तुमचे पूर्ण नाव"'),
    ('placeholder="10 अंकी नंबर / 10-digit number"', 'data-mr-placeholder="१० अंकी नंबर" data-en-placeholder="10-digit number" placeholder="१० अंकी नंबर"'),
    ('placeholder="चौकशीचा विषय / Subject of your query"', 'data-mr-placeholder="चौकशीचा विषय" data-en-placeholder="Subject of your query" placeholder="चौकशीचा विषय"'),
    ('placeholder="तुमची चौकशी तपशीलवार लिहा / Write your query in detail"', 'data-mr-placeholder="तुमची चौकशी तपशीलवार लिहा" data-en-placeholder="Write your query in detail" placeholder="तुमची चौकशी तपशीलवार लिहा"'),
]

# Options
options = [
    ('<option value="general">सामान्य चौकशी / General Inquiry</option>', '<option value="general" data-mr="सामान्य चौकशी" data-en="General Inquiry">सामान्य चौकशी</option>'),
    ('<option value="scheme">योजना माहिती / Scheme Information</option>', '<option value="scheme" data-mr="योजना माहिती" data-en="Scheme Information">योजना माहिती</option>'),
    ('<option value="complaint">तक्रार / Complaint</option>', '<option value="complaint" data-mr="तक्रार" data-en="Complaint">तक्रार</option>'),
    ('<option value="suggestion">सूचना / Suggestion</option>', '<option value="suggestion" data-mr="सूचना" data-en="Suggestion">सूचना</option>'),
]

for old, new in replacements + placeholders + options:
    html = html.replace(old, new)


# JS fixes in script handling forms
js_fixes = [
    ("showError('कृपया नाव प्रविष्ट करा / Please enter your name');", "showError(lang === 'mr' ? 'कृपया नाव प्रविष्ट करा' : 'Please enter your name');"),
    ("showError('कृपया फोन नंबर प्रविष्ट करा / Please enter phone number');", "showError(lang === 'mr' ? 'कृपया फोन नंबर प्रविष्ट करा' : 'Please enter phone number');"),
    ("showError('कृपया वैध 10 अंकी फोन नंबर प्रविष्ट करा / Please enter valid 10-digit phone number');", "showError(lang === 'mr' ? 'कृपया वैध 10 अंकी फोन नंबर प्रविष्ट करा' : 'Please enter valid 10-digit phone number');"),
    ("showError('कृपया विषय प्रविष्ट करा / Please enter subject');", "showError(lang === 'mr' ? 'कृपया विषय प्रविष्ट करा' : 'Please enter subject');"),
    ("showError('कृपया संदेश प्रविष्ट करा / Please enter your message');", "showError(lang === 'mr' ? 'कृपया संदेश प्रविष्ट करा' : 'Please enter your message');"),
    ('<span>पाठवत आहे... / Submitting...</span>', '<span class="lang-mr">पाठवत आहे...</span><span class="lang-en">Submitting...</span>'),
    ('<span>चौकशी पाठवा / Submit Query</span>', '<span class="lang-mr">चौकशी पाठवा</span><span class="lang-en">Submit Query</span>')
]

for old, new in js_fixes:
    html = html.replace(old, new)


# We need to insert the CSS
css_insert = """
    <style>
        /* Language Toggle Classes */
        html[lang="mr"] .lang-en { display: none !important; }
        html[lang="en"] .lang-mr { display: none !important; }
"""
html = html.replace('<style>', css_insert, 1)

# Modify navbar to add language toggle button
nav_insert = """
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
"""

nav_replace = """
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
"""

# Actually, the right side has mobile menu button. Let's insert toggle button next to it.
btn_old = """
                <!-- Mobile Menu Button -->
                <button id="mobile-menu-btn"
"""
btn_new = """
                <!-- Language Toggle Button -->
                <div class="flex items-center gap-2 mr-2 md:mr-0 md:ml-4 flex-shrink-0">
                    <button id="lang-toggle-btn" class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 transition-colors border border-slate-200" aria-label="Toggle Language">
                        <i data-lucide="languages" class="w-4 h-4 text-primary-base"></i>
                        <span class="text-sm font-semibold text-primary-base" id="lang-toggle-text">EN</span>
                    </button>
                </div>

                <!-- Mobile Menu Button -->
                <button id="mobile-menu-btn"
"""
html = html.replace(btn_old, btn_new)

# Modify JS to handle form error logic `const lang = document.documentElement.lang;`
js_submit = """
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const lang = document.documentElement.lang;
            // Get form values
"""
html = html.replace("contactForm.addEventListener('submit', function(e) {\n            e.preventDefault();\n            \n            // Get form values", js_submit)

js_toggle = """
        // Language Toggle
        const langToggleBtn = document.getElementById('lang-toggle-btn');
        const langToggleText = document.getElementById('lang-toggle-text');
        const htmlElement = document.documentElement;

        function updateDynamicContent(lang) {
            // Update placeholders
            document.querySelectorAll(`[data-${lang}-placeholder]`).forEach(el => {
                el.placeholder = el.getAttribute(`data-${lang}-placeholder`);
            });
            // Update options
            document.querySelectorAll(`option[data-${lang}]`).forEach(el => {
                el.textContent = el.getAttribute(`data-${lang}`);
            });
        }

        langToggleBtn.addEventListener('click', () => {
            const currentLang = htmlElement.getAttribute('lang');
            const newLang = currentLang === 'mr' ? 'en' : 'mr';
            
            htmlElement.setAttribute('lang', newLang);
            langToggleText.textContent = newLang === 'mr' ? 'EN' : 'MR';
            
            updateDynamicContent(newLang);
        });

        // Initialize dynamic content on load
        updateDynamicContent(htmlElement.getAttribute('lang') || 'mr');
"""
html = html.replace("// Initialize Lucide Icons", js_toggle + "\n        // Initialize Lucide Icons")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully.")
