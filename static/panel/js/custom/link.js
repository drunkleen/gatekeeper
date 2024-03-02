function toggleAllQRCode() {
    const qrcodeDivs = document.querySelectorAll('[id^="qrcode"]');
    qrcodeDivs.forEach(function (qrcodeDiv) {
        qrcodeDiv.style.display = (qrcodeDiv.style.display === 'none' || qrcodeDiv.style.display === '') ? 'block' : 'none';
    });
}

function copyText() {
    const text = "{{ scheme_host }}{% url 'user_link_page_show' link.subscription_uuid %}"

    navigator.clipboard.writeText(text).then(function() {
    }).catch(function(err) {
        console.error('Unable to copy text', err);
    });
}