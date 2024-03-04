<p align="center">
  <a href="https://github.com/drunkleen/gatekeeper/" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="160" height="160" src="./static/panel/media/logos/Logo.png">
    </picture>
  </a>
</p>

<h1 align="center">گیت‌کیپر</h1>

<p align="center">
    یک راه حل برای مدیریت و حفاظت از پنل و لینک‌های شما.
</p>
<p align="center">
    <a href="./README.md">ENGLISH</a> | <a href="./README-fa.md">فارسی</a>
</p>

<br/>
<p align="center">
    <a href="https://github.com/drunkleen/gatekeeper/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/drunkleen/gatekeeper?style=flat-square" />
    </a>
    <a href="https://www.youtube.com/@drunkleen/" target="_blank">
        <img src="https://img.shields.io/badge/youtube-channel-crimson?style=flat-square&logo=youtube" />
    </a>
    <a href="https://twitter.com/DrunkLeen">
        <img src="https://img.shields.io/badge/twitter-page-blue?style=flat-square&logo=x" />
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/stars/drunkleen/gatekeeper?style=social" />
    </a>
</p>

<p align="center">
  <a href="https://github.com/drunkleen/gatekeeper/" target="_blank" rel="noopener noreferrer" >
    <img src="./static/panel/media/logos/showcase.png" alt="Showcase screenshots" width="600" height="auto">
  </a>
</p>

## معرفی

گیت‌کیپر یک ابزار مدیریت لینک‌ به زبان پایتون است که یک رابط کاربری ساده برای مدیریت و کنترل دسترسی به
لینک‌های v2ray و سایر VPN‌ها فراهم می‌کند. با گیت‌کیپر، شما می‌توانید به راحتی دسترسی به لینک‌ها را برای کاربران مجاز و
در اینترنت
محدود کنید و امنیت پنل‌های خود را تضمین کنید.

### ویژگی‌ها

- سازگاری جامع با سه
  پنل : [Marzban](https://github.com/Gozargah/Marzban), [3x-ui MHSanaei](https://github.com/MHSanaei/3x-ui)
  و [x-ui alireza0](https://github.com/alireza0/x-ui).
- قابلیت مدیریت بهتر لینک‌ها و کاربران.
- ایجاد کد QR داخلی برای تعامل بی‌دردسر.
- حفاظت قوی برای لینک‌ها و تنظیمات اشتراک.
- و بسیاری ویژگی‌های دیگر که یک مجموعه جامع فراهم می‌آورد.

## راهنمای نصب

1. دستور زیر را اجرا کنید

```bash
sudo bash -c "$(curl -sSL https://raw.githubusercontent.com/drunkleen/gatekeeper/master/install_script.sh)" @ install
```

پس از نصب موفق:

2. نمایش لاگ را با بستن ترمینال یا فشردن `Ctrl+C` متوقف کنید.

3. تنظیمات را در فایل تنظیمات `/opt/gatekeeper/.env` پیدا کنید و محتوای آن را به نیاز خود تغییر دهید.

4. پنل گیت‌کیپر را با اجرای دستور `gatekeeper restart` بعد از اعمال تغییرات در
   /opt/gatekeeper/.env دوباره راه‌اندازی کنید.

5. یک حساب مدیریتی با دستور `gatekeeper createadmin` ایجاد کنید.

6. به وسیله مرورگر وارد پنل گیت‌کیپر شوید: `http://YOUR_SERVER_IP:2087/auth/sign-in` (YOUR_SERVER_IP را با آدرس IP واقعی
   سرور خود جایگزین کنید).

7. در این مرحله فرآیند نصب به پایان می‌رسد! حالا با استفاده از اطلاعات حساب مدیریتی خود وارد پنل شوید.

دستور زیر را برای باز کردن منوی راهنمای کمکی اجرا کنید.

```bash
gatekeeper --help
```

| **لطفاً توجه داشته باشید که هنگام ایجاد حساب کاربری در پنل ادمین در لیست کاربران، رمز عبور پیش‌فرض به طور خودکار به `Gatekeeper2024@` تنظیم می‌شود.** |
|-------------------------------------------------------------------------------------------------------------------------------------------------------|

## پیکربندی

تنظیمات را با استفاده از متغیرهای محیطی یا قرار دادن آنها در فایل `.env` پیکربندی کنید.

برای این کار، فایل `.env` را که در `/opt/gatekeeper/` قرار دارد با ویرایشگر متن مورد علاقه خود، برای مثال `nano` یا `vim` باز کنید.

| متغیر               | توضیحات                                                                     |
|---------------------|-----------------------------------------------------------------------------|
| DEBUG               | فعال کردن حالت اشکال‌زدایی برای توسعه (پیش‌فرض: `False`)                    |
| ALLOWED_HOSTS       | مشخص کردن میزبان برای متصل کردن برنامه (پیش‌فرض: `any`)                     |
| SERVER_PORT         | اختصاص پورت به برنامه (پیش‌فرض: `2087`)                                     |
| SET_EMAIL           | آیا می‌خواهید از ایمیل برای ارسال ایمیل‌ها استفاده کنید؟ (پیش‌فرض: `False`) |
| EMAIL_HOST          | میزبان ایمیل شما (مثلاً `smtp.gmail.com`)                                   |
| EMAIL_PORT          | پورت ایمیل شما (مثلاً `587`)                                                |
| EMAIL_USE_TLS       | فعال کردن TLS برای ارتباط ایمیل (پیش‌فرض: `True`)                           |
| EMAIL_HOST_USER     | نام کاربری/آدرس ایمیل شما (مثلاً `example@gmail.com`)                       |
| EMAIL_HOST_PASSWORD | رمز عبور ایمیل شما (مثلاً `password`).                                      |

## لیست کارها

1. [x] **اصلاح اسکریپت Bash:** مشکلات و بهینه‌سازی اسکریپت Bash موجود را برطرف کنید.
2. [ ] **اصلاح رابط کاربری (UI):** مشکلات یا بهبود طراحی رابط کاربری را برطرف کنید.
3. [ ] **اضافه کردن پشتیبانی چندزبانگی:** ترجمه‌ها را برای چند زبان اجرا کرده و پروژه خود را قابل دسترسی بیشتر کنید.
4. [ ] **حذف داده‌ها و کدهای اضافی:** عناصر غیرضروری را در داده و کد برای بهبود کارایی و خوانایی بهتر برش کنید.
5. [ ] **بازنگری کد:** ساختار و کد پروژه را برای دسترسی و بهره‌وری بهتر بازبینی کنید.
6. [ ] **اضافه کردن پشتیبانی برای پنل‌های دیگر:** سازگاری را با اضافه کردن پشتیبانی برای پنل‌های رابط کاربری دیگر گسترش
   دهید.
7. [ ] **اضافه کردن پشتیبانی‌های دیگر:** ویژگی‌ها یا پشتیبانی‌های اضافی را ارزیابی و ادغام کنید تا قابلیت‌های پروژه خود
   را بهبود بخشید.
8. [ ] **مستندسازی:** دستورالعمل‌های نصب، اجرا و استفاده از پروژه خود را ارائه دهید.

## چگونگی همکاری

اگر می‌خواهید به پروژه همکاری کنید، این مراحل را دنبال کنید:

1. پروزه را فورک کنید.
2. `git checkout -b feature/new-feature` :یک برنچ جدید بسازید
3. `git commit -m 'Add a new feature'` :تغییرات خود را کامیت کنید
4. `git push origin feature/new-feature` :به برنچ بروید
5. باز کنید Pull Request یک

## اهدای مالی

اگر گیت‌کیپر برای شما کاربردی یوده و می‌خواهید به بهبود و توسعه‌اش کمک کنید، از حمایت شما سپاسگزاریم. شما می‌توانید از
طریق [PayPal](https://www.paypal.com/paypalme/RDarvishifar) یا هر یک از شبکه‌های رمزارز زیر حمایت خود را نشان دهید:

- **Bitcoin (BTC):** `bc1qsmvxpn79g6wkel3w67k37r9nvzm5jnggeltxl6`
- **ETH/BNB/MATIC (ERC20, BEP20):** `0x8613aD01910d17Bc922D95cf16Dc233B92cd32d6`
- **USDT/TRON (TRC20):** `TGNru3vuDfPh5zBJ31DKzcVVvFgfMK9J48`
- **Dogecoin (DOGE):** `D8U25FjxdxdQ7pEH37cMSw8HXBdY1qZ7n3`

مشارکت شما به بهبود و پشتیبانی مداوم گیت ‌کیپر را زنده نگه میدارد.

با تشکر از حمایت شما!

## قدردانی:

این پنل بر اساس قالب HTML رایگان SAUL از "[KeenThemes](https://keenthemes.com/)" ساخته شده است.

## مجوز

این پروژه تحت مجوز [GNU v3.0](./LICENSE) است - برای جزئیات بیشتر [LICENSE](./LICENSE) را ببینید.