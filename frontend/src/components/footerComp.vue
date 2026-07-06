<script setup>
import { CONTACTS } from '../constants.js'
import LogoComp from '@/components/LogoComp.vue'
</script>

<template>
  <footer class="footer" id="footer">
    <div class="container">
      <div class="footer-inner">

        <!-- Brand column -->
        <div class="footer-brand">
          <a class="brandmark" href="/" aria-label="MFS Fleet">
            <span class="glyph">
              <LogoComp style="width:70px;height:auto" />
            </span>
            <span>Fleet <span class="sub">· {{ $t('brand.country') }}</span></span>
          </a>
          <p>{{ $t('footer.description') }}</p>
          <div class="socials">
            <a :href="CONTACTS.TELEGRAM" class="social" aria-label="Telegram" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M21.7 3.3 2.6 10.8c-1 .4-1 1 .2 1.3l4.9 1.5 1.9 6c.2.7.4.9.9.9.4 0 .6-.2.9-.5l2.4-2.3 4.9 3.6c.9.5 1.5.3 1.8-.9l3.3-15.5c.3-1.3-.5-1.9-1.4-1.6zM9.8 14.7l9.5-6c.5-.3.9 0 .5.4l-7.8 7.1-.3 3.2-1.9-4.7z"/></svg>
            </a>
            <a :href="CONTACTS.INSTAGRAM" class="social" aria-label="Instagram" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>
            </a>
            <a :href="'mailto:' + CONTACTS.EMAIL" class="social" aria-label="Email">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            </a>
          </div>
        </div>

        <!-- Contacts column -->
        <div>
          <h5>{{ $t('footer.contacts-title') }}</h5>
          <ul>
            <li><a :href="'tel:' + CONTACTS.PHONE.replace(/\s/g, '')">{{ CONTACTS.PHONE }}</a></li>
            <li><a :href="CONTACTS.TELEGRAM" target="_blank" rel="noopener">Telegram: @MFS_support</a></li>
            <li><a :href="'mailto:' + CONTACTS.EMAIL">may.fleet.solutions@&#8203;gmail.com</a></li>
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
  width: 44px;
  height: 44px;
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
