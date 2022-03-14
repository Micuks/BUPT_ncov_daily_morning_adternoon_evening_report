# 每日填报晨午晚检

## 使用方法

1.点击 `Use this template` 来从这个模板创建新仓库.

2.在 `Settings/Secrets/Actions` 中点击 `New repository secret` 来创建以下`Actions Secrets`:

- `USERNAME`: 你的学号
- `PASSWORD`: 你的密码

之后,`Github Actions`会自动在北京时间8点, 12点和18点填报.

如果你想手动运行,可以进入`Actions`栏,点击`Re-run Jobs`来重新运行,或者执行一次`git push`操作.

> 当你移动了位置后,需要手动填报一次,才能正常运行.

## 关于更改填报时间

可以在`.github/workflow/main.yml`中设置每天的运行时间:

```
on:
	schedule:
		- cron: "2/8 0 * * *"
		- cron: "2/8 4 * * *"
		- cron: "2/8 10 * * *"
```
时间格式为cron格式,如`"2/8 0 * * *"`意为每天的北京时间8点2分开始,每隔8分钟尝试填报一次,直到北京时间8点58分,共尝试8次.
