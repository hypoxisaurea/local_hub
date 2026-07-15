<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>Local Hub</h4>
        <p>지역의 숨겨진 보석들을 발견하세요.</p>
      </div>

      <div class="footer-section">
        <h4>메뉴</h4>
        <ul>
          <li><RouterLink to="/">홈</RouterLink></li>
          <li><RouterLink to="/community">커뮤니티</RouterLink></li>
          <li><RouterLink to="/travel">여행지</RouterLink></li>
          <li><RouterLink to="/restaurant">맛집</RouterLink></li>
          <li><RouterLink to="/festival">축제</RouterLink></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>고객지원</h4>
        <ul>
          <li><a href="#">공지사항</a></li>
          <li><a href="#">FAQ</a></li>
          <li><a href="#">문의하기</a></li>
          <li><a href="#">이용약관</a></li>
          <li><a href="#">개인정보처리방침</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>팔로우</h4>
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
// Footer 로직 필요시 여기에 추가
</script>

<style scoped>
.footer {
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
  color: #ff6b6b;
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
  color: #ff6b6b;
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
  background-color: #ff6b6b;
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