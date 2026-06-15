<template>
  <footer class="footer" id="footer">
    <div class="container">
      <div class="footer-inner">

        <!-- Brand column -->
        <div class="footer-brand">
          <a class="brandmark" href="/" aria-label="MFS Fleet">
            <span class="glyph">
              <svg fill="currentColor" aria-hidden="true" viewBox="0 19 78 31" style="width:70px;height:auto">
                <path d="M36.917 35.4791L37.782 30.2397H49.535L48.67 35.4791H36.917Z"/>
                <path d="M53.8181 29.4093H53.6709L53.6919 29.2729L53.8181 29.4093Z"/>
                <path d="M70.7841 39.9395L70.7809 39.9679L70.7554 39.9395H70.7841Z"/>
                <path d="M70.8437 40.0365H70.7673L70.7795 39.9668L70.8437 40.0365Z"/>
                <path d="M54.5569 19.3517H38.8032L38.8092 19.3184H34.9646L29.438 24.5426L25.23 50.0002H33.7391L37.9381 24.5911H53.6919L54.5569 19.3517Z"/>
                <path d="M60.9367 29.2728L61.7476 24.3637H69.2686L70.0976 19.3516H55.332L53.692 29.2728L53.8182 29.4091L63.6189 39.9394H63.5378L62.7028 44.9879H54.7072L55.5392 39.9394H48.2946L46.6306 50H69.1184L70.7794 39.9667L70.7554 39.9394L60.9367 29.2728Z"/>
                <path d="M70.9145 19.3516L69.2505 29.4091H76.3389L77.9999 19.3516H70.9145Z"/>
                <path d="M19.319 34.1184L9.15792 19.3184H5.07004L0 50.0002H8.6413L11.4316 33.0487L16.772 40.0881H20.3372L27.2245 33.0002L28.4709 25.4608L19.319 34.1184Z"/>
              </svg>
            </span>
            <span>Fleet <span class="sub">· {{ $t('brand.country') }}</span></span>
          </a>
          <p>{{ $t('footer.description') }}</p>
          <div class="socials">
            <a href="https://t.me/MFS_support" class="social" aria-label="Telegram" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M21.7 3.3 2.6 10.8c-1 .4-1 1 .2 1.3l4.9 1.5 1.9 6c.2.7.4.9.9.9.4 0 .6-.2.9-.5l2.4-2.3 4.9 3.6c.9.5 1.5.3 1.8-.9l3.3-15.5c.3-1.3-.5-1.9-1.4-1.6zM9.8 14.7l9.5-6c.5-.3.9 0 .5.4l-7.8 7.1-.3 3.2-1.9-4.7z"/></svg>
            </a>
            <a href="https://www.instagram.com/mfs_cz" class="social" aria-label="Instagram" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>
            </a>
            <a href="mailto:may.fleet.solutions@gmail.com" class="social" aria-label="Email">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            </a>
          </div>
        </div>

        <!-- Contacts column -->
        <div>
          <h5>{{ $t('footer.contacts-title') }}</h5>
          <ul>
            <li><a href="tel:+420775995339">+420 775 995 339</a></li>
            <li><a href="https://t.me/MFS_support" target="_blank" rel="noopener">Telegram: @MFS_support</a></li>
            <li><a href="mailto:may.fleet.solutions@gmail.com">may.fleet.solutions@&#8203;gmail.com</a></li>
          </ul>
        </div>

        <!-- Nav column -->
        <div>
          <h5>{{ $t('footer.service-title') }}</h5>
          <ul>
            <li><a href="/#features">{{ $t('footer.links.features') }}</a></li>
            <li><a href="/#how">{{ $t('footer.links.how') }}</a></li>
            <li><a href="/#vehicles">{{ $t('footer.links.transport') }}</a></li>
            <li><a href="/form">{{ $t('landing.cta.apply') }}</a></li>
          </ul>
        </div>

      </div>

      <div class="copyright">
        <span>{{ $t('footer.copyright') }}</span>
        <span>{{ $t('footer.made-in') }}</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--bg-2);
  border-top: 1px solid var(--border);
  padding: clamp(40px, 6vw, 72px) 0 28px;
}

.footer-inner {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 32px 48px;
}

.brandmark {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: 17px;
  letter-spacing: -.01em;
  color: var(--text);
  text-decoration: none;
}

.glyph {
  height: 38px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 4px;
}

.sub {
  color: var(--text-3);
  font-weight: 500;
  font-family: var(--font-sans);
  font-size: 13px;
}

.footer-brand p {
  color: var(--text-2);
  font-size: 14px;
  max-width: 340px;
  margin-top: 14px;
  line-height: 1.55;
}

h5 {
  font-family: var(--font-sans);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 14px;
}

ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

a {
  color: var(--text-2);
  transition: color var(--t-fast);
  font-size: 14.5px;
  text-decoration: none;
}
a:hover { color: var(--text); }

.socials {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}

.social {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  display: grid;
  place-items: center;
  color: var(--text-2);
  transition: color var(--t-fast), background-color var(--t-fast), border-color var(--t-fast), transform var(--t-fast);
}
.social:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: translateY(-2px);
}

.copyright {
  margin-top: 40px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 12px;
  color: var(--text-3);
  font-size: 12.5px;
}

@media (max-width: 860px) {
  .footer-inner { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 520px) {
  .footer-inner { grid-template-columns: 1fr; }
}
</style>
