<p align="center">
  <a href="https://github.com/drunkleen/gatekeeper/" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="160" height="160" src="./static/panel/media/logos/Logo.png">
    </picture>
  </a>
</p>

<h1 align="center">Gate Keeper</h1>

<p align="center">
    一个用于管理和保护面板和链接的解决方案。
</p>
<p align="center">
    <a href="./README.md">ENGLISH</a> | <a href="./README-fa.md">فارسی</a> | <a href="./README-ru.md">Русский </a> | <a href="./README-zh.md">中文</a>
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

## 概览

GateKeeper 是一个用Python制作的直观链接管理工具，提供了一个用户友好的界面，用于无缝管理和控制v2ray/其他VPN链接。通过GateKeeper，您可以轻松地限制链接访问权限，确保对面板的增强安全性。

### 特性

- 与三个主要面板完全兼容：
  [Marzban](https://github.com/Gozargah/Marzban),
  [3x-ui MHSanaei](https://github.com/MHSanaei/3x-ui) 和
  [x-ui alireza0](https://github.com/alireza0/x-ui)。
- 增强的链接和用户管理功能。
- 内置QR码生成器，实现无缝互动。
- 强大的配置/订阅链接保护。
- 还有更多功能，确保全面的功能集。

## 安装指南

1. 运行以下命令

```bash
sudo bash -c "$(curl -sSL https://raw.githubusercontent.com/drunkleen/gatekeeper/master/install_script.sh)" @ install
```

安装成功后：

2. 通过关闭终端或按`Ctrl+C`终止日志查看。

3. 找到位于`/opt/gatekeeper/.env`的配置文件，并根据需要修改其内容。

4. 在对`/opt/gatekeeper/.env`进行修改后，通过执行`gatekeeper restart`命令重新启动GateKeeper面板。

5. 使用`gatekeeper createadmin`命令生成管理员帐户。

6. 通过浏览器访问`http://YOUR_SERVER_IP:2087/auth/sign-in`（用服务器的实际IP地址替换`YOUR_SERVER_IP`）来访问GateKeeper仪表板。

7. 这就完成了！现在，使用管理员帐户的凭据登录到您的仪表板。

如需获取有关GateKeeper脚本的帮助，请执行以下命令以访问帮助消息。

```bash
gatekeeper --help
```

| **请注意，使用管理员权限在用户列表中创建用户时，默认密码会自动设置为 `Gatekeeper2024@`。** |
|----------------------------------------------------------|

## 配置

通过使用环境变量或将它们放在`.env`文件中进行配置设置。

为此，使用您喜欢的文本编辑器（如`nano`或`vim`）打开位于`/opt/gatekeeper/`的`.env`文件。

| 变量                  | 描述                                   |
|---------------------|--------------------------------------|
| DEBUG               | 为开发启用调试模式（默认：`False`）                |
| ALLOWED_HOSTS       | 指定应用绑定的主机（默认：`any`）                  |
| SERVER_PORT         | 分配应用到该端口（默认：`2087`）                  |
| SET_EMAIL           | 是否要使用电子邮件发送邮件（默认：`False`）            |
| EMAIL_HOST          | 您的电子邮件主机（例如，`smtp.gmail.com`）        |
| EMAIL_PORT          | 您的电子邮件端口（例如，`587`）                   |
| EMAIL_USE_TLS       | 启用TLS以进行电子邮件通信（默认：`True`）            |
| EMAIL_HOST_USER     | 您的电子邮件用户名/地址（例如，`example@gmail.com`） |
| EMAIL_HOST_PASSWORD | 您的电子邮件密码（例如，`password`）。             |

## 待办事项清单

1. [x] **修复Bash脚本：**解决问题并优化现有的Bash脚本。
2. [ ] **修复用户界面：**解决任何用户界面相关的问题或改善设计以提供更好的用户体验。
3. [ ] **添加多语言支持：**实施多语言翻译，使您的项目更易访问。
4. [ ] **删除多余的数据和代码：**剪裁不必要的元素，以提高效率和可读性。
5. [ ] **重构代码：**重新构建和改进整体代码库以提高可维护性和性能。
6. [ ] **添加对X-UI面板的支持：**通过支持额外的UI面板，扩展兼容性。
7. [ ] **实施其他支持：**评估并集成其他功能或支持，以增强项目的功能。
8. [ ] **文

档：**提供关于如何设置、运行和使用项目的说明。

## 如何贡献

如果您想为该项目做出贡献，请按照以下步骤进行：

1. Fork仓库。
2. 创建新分支：`git checkout -b feature/new-feature`。
3. 提交更改：`git commit -m '添加新功能'`。
4. 推送到分支：`git push origin feature/new-feature`。
5. 打开拉取请求。

## 捐赠

如果您发现GateKeeper有价值并希望为其持续发展做出贡献，我们非常感谢您的支持。您可以通过 [Paypal](https://www.paypal.com/paypalme/RDarvishifar)
或以下加密货币网络之一显示您的支持：

- **比特币 (BTC):** `bc1qsmvxpn79g6wkel3w67k37r9nvzm5jnggeltxl6`
- **ETH/BNB/MATIC (ERC20, BEP20):** `0x8613aD01910d17Bc922D95cf16Dc233B92cd32d6`
- **USDT/TRON (TRC20):** `TGNru3vuDfPh5zBJ31DKzcVVvFgfMK9J48`
- **狗狗币 (DOGE):** `D8U25FjxdxdQ7pEH37cMSw8HXBdY1qZ7n3`

您的慷慨捐赠确保了GateKeeper持续改进和维护。

感谢您支持这个项目！

## 致谢:

该面板是基于[KeenThemes](https://keenthemes.com/)慷慨提供的SAUL HTML免费模板构建的。

## 许可证

本项目根据 [GNU v3.0](./LICENSE) 许可证发布 - 请查看 [LICENSE](./LICENSE) 文件以获取详细信息。
