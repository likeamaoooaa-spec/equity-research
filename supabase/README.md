# Supabase 批注安全配置

网站只应使用 publishable/anon key；不要把 service-role key 写入前端或 Git。

请在 Supabase SQL Editor 中检查并应用 [rls.sql](rls.sql)。匿名用户可以读取公开批注和新增批注，但不能更新、删除或读取管理字段。生产环境还应在 Supabase 控制台配置 CAPTCHA、速率限制或审核队列。
