<template>
  <footer id="footer">
    <div>
      <span>MAY fleet solutions</span>
      <a href="https://t.me/MFS_support" target="_blank">telegram: @MFS_support</a>
      <a href="mailto:may.fleet.solutions@gmail.com" target="_blank">may.fleet.solutions@gmail.com</a>
      <a href="tel:+420733588688">+420 733 588 688</a>
      <nav>
        <a href="https://t.me/MFS_support" target="_blank">
          <img src="/telegramIcon.svg" alt="Telegram" />
        </a>
        <a href="https://www.instagram.com/mfs_cz?igsh=MWxpc3E5NG1yN3B5bQ==" target="_blank">
          <img src="/instagramIcon.svg" alt="Instagram" />
        </a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
footer {
  background-color: var(--brand-color);
  width: 100%;
  min-width: 700px;
  padding: 20px 40px;
  box-sizing: border-box;
}

footer > div {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}

span {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-text-color);
  white-space: nowrap;
}

footer > div > a {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 16px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-text-color);
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.2s ease;
}

footer > div > a:hover {
  opacity: 0.8;
}

nav {
  display: flex;
  align-items: center;
  gap: 16px;
}

nav a {
  display: flex;
  align-items: center;
  transition: opacity 0.2s ease;
}

nav a:hover {
  opacity: 0.8;
}

nav img {
  height: 28px;
  width: 28px;
}
</style>
