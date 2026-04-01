<template>
    <section class="mobile-footer-strip">
      <div class="mobile-footer-copy">
        <p>MAY fleet solutions</p>
        <a class="app-fade-transition" href="tel:+420733588688">+420 733 588 688</a>
        <a class="app-fade-transition" href="https://t.me/MFS_support" target="_blank" rel="noreferrer">
          telegram: @MFS_support
        </a>
        <a class="app-fade-transition" href="mailto:may.fleet.solutions@gmail.com">
          may.fleet.solutions@gmail.com
        </a>
      </div>

      <div class="mobile-footer-icons">
        <a
          class="app-fade-transition"
          href="https://t.me/MFS_support"
          target="_blank"
          rel="noreferrer"
          aria-label="Telegram"
        >
          <img src="/telegramIcon.svg" alt="" />
        </a>
        <a
          class="app-fade-transition"
          href="https://www.instagram.com/mfs_cz?igsh=MWxpc3E5NG1yN3B5bQ=="
          target="_blank"
          rel="noreferrer"
          aria-label="Instagram"
        >
          <img src="/instagramIcon.svg" alt="" />
        </a>
      </div>
    </section>
</template>

<style scoped>
.mobile-footer-strip {
  margin-top: 28px;
  padding: 18px 12px 22px;
  background-color: var(--brand-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.mobile-footer-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-footer-copy p,
.mobile-footer-copy a {
  margin: 0;
  color: var(--brand-text-color);
  text-decoration: none;
  font-weight: 700;
  font-size: clamp(11px, 3.6vw, 14px);
  line-height: 1.15;
}

.mobile-footer-copy a:hover {
  opacity: 0.8;
}

.mobile-footer-icons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mobile-footer-icons a {
  display: inline-flex;
  align-items: center;
}

.mobile-footer-icons a:hover {
  opacity: 0.8;
}

.mobile-footer-icons img {
  width: 30px;
  height: 30px;
}
</style>