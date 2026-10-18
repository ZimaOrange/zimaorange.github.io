# 山的另一面，是梦

齐马橙 ZimaOrange 的藏汉双语互动作品集。包含 161 幅作品、滚动叙事和环境音。

## 内容

GitHub Actions 按 `.github/workflows/deploy.yml` 中的顺序解压作品集与增量资源，并发布到 GitHub Pages。当前首页和作品详情的最终版本来自 `portfolio-polish.zip`；仓库根目录的 `index.html` 不是最终发布层。旧归档继续保留，请勿改变现有归档的顺序或校验值。

## 实验交互

- 栏目：`/experiments/`
- 潮汐回响：`/experiments/tidal-echoes/`

实验栏目与交互作品保存在 `experiments-v46.zip.part*` 中，按文件名顺序合并即可得到 ZIP。包内包含可编辑的栏目 HTML/CSS 和完整应用文件。新增发布步骤在所有原有作品集归档之后执行，先校验并解压实验包，再运行 `install-experiments.py`，为原有首页和七个作品详情页加入「实验交互」链接。

`install-experiments.py` 不改动原有作品内容、脚本、资源路径或域名配置；重复执行不会产生重复链接。缺少任一作品页或应用入口时，它会停止发布。更新实验包后，必须同时更新工作流中的 SHA-256 校验值。向 `main` 推送会触发现有 GitHub Pages 工作流，无需改 DNS。

本地检查新增入口：`python3 -m unittest discover -s tests -v`（测试文件随开发 checkout 保存）。最终发布前，还需检查完整解压后的首页、窄屏导航、实验栏目、作品入口、摄像头与录制功能。

网站无需后台服务。原作影像版权归齐马橙所有，未授予转载或商业使用许可。藏文标题为暂译，待母语校对。

## 背景音乐更新（v47）

`experiments-v47.zip` 是 v46 之后的小型增量层，只覆盖修改过的应用文件和栏目文字。音乐现在仅作背景播放，不驱动粒子、奇点、镜头或爆发效果；手势玩法继续保留。发布时先解压 v46，再校验并覆盖 v47。无需重新上传未改动的音乐、模型、WebAssembly 或图片资源。
