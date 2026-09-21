# Как тестировать текущую сборку GovPro AI

На текущем этапе тестировать интерфейс уже можно локально, без production backend.

## Windows Preview

В инженерном репозитории откройте файл Start-GovPro-Preview.cmd.

Preview запускает desktop UI в демонстрационном режиме. Он не требует Supabase, PostgreSQL или GovPro Model.

Проверять можно:

- внешний вид и плотность интерфейса;
- Ассистент / Дела / Законы;
- Server Profile;
- режимы БАЗА / ОФИЦЕР / КРАЙМ / АДВОКАТ / ПРОКУРОР;
- чат и структуру ответа;
- прикрепление изображения;
- настройки и состояния соединения.

Ответы Preview демонстрационные и не являются реальными нормами.

## Проверка кода

Из корня инженерного репозитория:

python scripts/verify_local.py

Gate выполняет Python tests, frontend build и Rust/Tauri check при наличии Rust.

## Что пока нельзя считать готовым

Полноценное production-тестирование реальных ответов ещё зависит от PostgreSQL/Supabase, опубликованной Knowledge Base и GovPro Model runtime. Stable также остаётся заблокированным до завершения signing и production gate.
