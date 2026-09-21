# Production Gate GovPro AI

Этот документ — технический gate перед публикацией пользовательской версии. Он не является юридическим заключением и не заменяет security/privacy review.

## Beta

Перед Beta должны быть выполнены:

- инженерный commit зафиксирован и указан в release metadata;
- Python tests проходят;
- frontend build проходит;
- Tauri/Rust check проходит, если Rust доступен в CI;
- Windows x64, macOS Intel, macOS Apple Silicon и Linux x64 сборки создаются;
- в релизе есть только ожидаемые установочные артефакты;
- SHA256SUMS.txt опубликован;
- RELEASE_METADATA.json опубликован;
- source commit одинаковый у всех платформ;
- release notes содержат разделы «Новое», «Улучшено», «Исправлено», «Безопасность», «Установка»;
- channel JSON проходит автоматическую валидацию;
- updater не должен доверять HTML GitHub Releases.

## Stable

Stable дополнительно требует:

- постоянный production signing key;
- проверку подписи installer/update metadata;
- подтверждённый rollback path;
- security review;
- проверку production authentication и tenant isolation;
- проверку актуальности Knowledge Base;
- production smoke-test реального AI runtime;
- проверку privacy controls для документов и изображений;
- зафиксированную политику хранения и удаления данных;
- проверку всех пользовательских ссылок на релиз и артефакты.

Пока signing и production smoke-test не завершены, Stable должен оставаться заблокированным.

## Update Center

channels/stable.json и channels/beta.json являются машинным контрактом Update Center.

Для опубликованного канала обязательны:

- product;
- channel;
- status;
- latest.version;
- latest.source_ref;
- latest.release_url;
- latest.published_at;
- latest.signature_status;
- latest.artifacts[].

Каждый артефакт должен иметь имя, размер, SHA-256 и прямой download_url.

Приватные секреты и ключи подписи не допускаются в репозитории.
