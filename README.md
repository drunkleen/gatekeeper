<p align="center">
  <a href="https://github.com/drunkleen/gatekeeper/" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="160" height="160" src="./static/panel/media/logos/Logo.png">
    </picture>
  </a>
</p>

<h1 align="center"/>Gate Keeper</h1>

<p align="center">
    A solution to safeguard your subscription links.
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

## Overview

GateKeeper is an intuitive link management tool crafted in Python, offering a user-friendly interface for seamless
management and access control of v2ray/other VPN links. With GateKeeper, you can effortlessly restrict link access to
authorized users, ensuring enhanced security for your panels.

### Features

- Comprehensive compatibility with three prominent
  panels: [Marzban](https://github.com/Gozargah/Marzban), [3x-ui MHSanaei](https://github.com/MHSanaei/3x-ui)
  and [x-ui alireza0](https://github.com/alireza0/x-ui)
- Enhanced link and user management capabilities
- In-built QR code generator for seamless interaction
- Robust protection for configuration/subscription links
- And much more, ensuring a comprehensive feature set.

## Installation guide

1- Run the following command

```bash
sudo bash -c "$(curl -sSL https://raw.githubusercontent.com/drunkleen/gatekeeper/master/install_script.sh)" @ install
```

Upon successful installation:

2 - Terminate log viewing by closing the terminal or pressing `Ctrl+C`.

3 - Locate the configuration file at `/opt/gatekeeper/.env` and modify its contents as needed.

4 - Restart the GateKeeper panel by executing the gatekeeper restart command after making modifications to
/opt/gatekeeper/.env.

5 - Generate an administrative account with the ```gatekeeper createadmin``` command.

6 - Access the GateKeeper dashboard via a web browser at `http://YOUR_SERVER_IP:8000/auth/sign-in` (replace
YOUR_SERVER_IP with your server's actual IP address).

7 - That concludes the process! Now, sign in to your dashboard using the credentials of your admin account.

For assistance with the GateKeeper script, execute the following command to access the help message.

```bash
gatekeeper --help
```

| **Please note that when creating users with admin privileges in the user list, the default password is automatically set to `Gatekeeper2024@`.** |
|--------------------------------------------------------------------------------------------------------------------------------------------------|

## Configuration

Configure the settings by utilizing environment variables or by placing them in the `.env` file.

To achieve this, open the `.env` file located at `/opt/gatekeeper/` using your preferred text editor, such as `nano`
or `vim`, for instance.

| Variable            | Description                                                              |
|---------------------|--------------------------------------------------------------------------|
| DEBUG               | Enable debug mode for development (default: `False`)                     |
| ALLOWED_HOSTS       | Specify the host for application binding (default: `any`)                |
| SERVER_PORT         | Assign the application to this port (default: `2087`)                    |
| SET_EMAIL           | Whether you're want to use an email for sending mails (default: `False`) |
| EMAIL_HOST          | Your email host (e.g., `smtp.gmail.com`)                                 |
| EMAIL_PORT          | Your email port (e.g., `587`)                                            |
| EMAIL_USE_TLS       | Enabling TLS for email communication (default: `True`)                   |
| EMAIL_HOST_USER     | Your email username/address (e.g., `example@gmail.com`)                  |
| EMAIL_HOST_PASSWORD | Your email password (e.g., `password`).                                  |

## To-Do List

Use this checklist to keep track of the tasks you need to accomplish for your project.

- [x] **Fix Bash Script:** Address issues and optimize the existing Bash script.
- [ ] **Fix UI:** Resolve any user interface-related issues or enhance the design for a better user experience.
- [ ] **Add Multilanguage Support:** Implement translations for multiple languages to make your project more accessible.
- [ ] **Remove Excess Data and Code:** Trim unnecessary elements in both data and code for better efficiency and
  readability.
- [ ] **Refactor the Code:** Restructure and improve the overall codebase for maintainability and performance.
- [ ] **Add Support for X-UI Panels:** Extend compatibility by incorporating support for additional UI panels.
- [ ] **Implement Other Supports:** Evaluate and integrate additional features or supports that enhance the
  functionality of your project.
- [ ] **Documentation:** Provide instructions on how to set up, run and use the project.

## How to Contribute

If you'd like to contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a pull request.

## Donation

If you've found GateKeeper valuable and wish to contribute to its ongoing development, you can show your support by
making a donation through [Paypal](https://www.paypal.com/paypalme/RDarvishifar) or any of the following cryptocurrency
networks:

- USDT/TRON (TRC20): `TGNru3vuDfPh5zBJ31DKzcVVvFgfMK9J48`
- ETH/BNB/MATIC (ERC20, BEP20): `0x8613aD01910d17Bc922D95cf16Dc233B92cd32d6`
- Bitcoin (BTC): `bc1qsmvxpn79g6wkel3w67k37r9nvzm5jnggeltxl6`
- Dogecoin (DOGE): `D8U25FjxdxdQ7pEH37cMSw8HXBdY1qZ7n3`

## Acknowledgment:

This panel is built upon the SAUL HTML free template generously provided by "[KeenThemes](https://keenthemes.com/)".

## License

This project is licensed under the [GNU v3.0](./LICENSE) - see the [LICENSE](./LICENSE) file for details.

