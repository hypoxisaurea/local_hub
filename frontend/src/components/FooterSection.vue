<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>Local Hub</h4>
        <p>{{ t('footer.description') }}</p>
      </div>

      <div class="footer-section">
        <h4>{{ t('footer.menu') }}</h4>
        <ul>
          <li><RouterLink to="/">{{ t('footer.home') }}</RouterLink></li>
          <li><RouterLink to="/community">{{ t('nav.community') }}</RouterLink></li>
          <li><RouterLink to="/travel">{{ t('nav.travel') }}</RouterLink></li>
          <li><RouterLink to="/restaurant">{{ t('nav.restaurant') }}</RouterLink></li>
          <li><RouterLink to="/festival">{{ t('nav.festival') }}</RouterLink></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>{{ t('footer.support') }}</h4>
        <ul>
          <li><a href="#">{{ t('footer.notice') }}</a></li>
          <li><a href="#">{{ t('footer.faq') }}</a></li>
          <li><a href="#">{{ t('footer.contact') }}</a></li>
          <li><a href="#">{{ t('footer.terms') }}</a></li>
          <li><a href="#">{{ t('footer.privacy') }}</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>{{ t('footer.follow') }}</h4>
        <div class="social-links">
          <a href="#" class="social-icon">Facebook</a>
          <a href="#" class="social-icon">Twitter</a>
          <a href="#" class="social-icon">Instagram</a>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 Local Hub. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.footer {
  --color-pink-600: oklch(59.2% 0.249 0.584);
  background-color: #333;
  color: #fff;
  padding: 40px 20px 20px;
  margin-top: 60px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  max-width: 1200px;
  margin: 0 auto 30px;
  gap: 30px;
}

.footer-section h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: var(--color-pink-600);
}

.footer-section p {
  font-size: 14px;
  line-height: 1.6;
  color: #bbb;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #bbb;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: var(--color-pink-600);
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-icon {
  display: inline-block;
  width: 35px;
  height: 35px;
  background-color: #555;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  font-size: 12px;
  transition: background-color 0.3s;
}

.social-icon:hover {
  color: var(--color-pink-600);
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #555;
  font-size: 13px;
  color: #999;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }

  .footer {
    padding: 30px 20px 15px;
  }
}
</style>
