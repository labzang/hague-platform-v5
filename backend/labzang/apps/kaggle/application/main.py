"""
Kaggle(Titanic) 서비스 진입점 (백워드 호환).
- 앱 생성·조립은 adapter/inbound/app.py에서 수행. 여기서는 재노출만.
"""
from labzang.apps.ml.adapter.inbound.app import app, config, run

if __name__ == "__main__":
    run()
