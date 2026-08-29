const snapshot = {
  date: "2026-08-26",
  source: "Banco Central Europeu",
  base: "EUR",
  rates: {
    EUR: 1,
    USD: 1.1669,
    JPY: 185.62,
    CZK: 24.083,
    DKK: 7.4757,
    GBP: 0.85613,
    HUF: 360.18,
    PLN: 4.2955,
    RON: 5.2568,
    SEK: 11.0785,
    CHF: 0.938,
    ISK: 141.2,
    NOK: 10.8845,
    TRY: 56.1481,
    AUD: 1.6241,
    BRL: 6.0055,
    CAD: 1.6176,
    CNY: 7.8422,
    HKD: 9.1463,
    IDR: 20668.66,
    ILS: 3.4706,
    INR: 111.3475,
    KRW: 1614.39,
    MXN: 19.7567,
    MYR: 4.6985,
    NZD: 1.9582,
    PHP: 71.952,
    SGD: 1.4817,
    THB: 38.21,
    ZAR: 18.5724
  }
};

const currencyNames = new Intl.DisplayNames(["pt-BR"], { type: "currency" });
const amountInput = document.querySelector("#amount");
const fromSelect = document.querySelector("#from-currency");
const toSelect = document.querySelector("#to-currency");
const resultValue = document.querySelector("#result-value");
const rateLine = document.querySelector("#rate-line");
const manualRateInput = document.querySelector("#manual-rate");
const manualFrom = document.querySelector("#manual-from");
const manualTo = document.querySelector("#manual-to");
const bridge = document.querySelector("#card-bridge");
const postConversion = document.querySelector("#post-conversion");
const internationalArticleCard = document.querySelector("#international-article-card");
const amountError = document.querySelector("#amount-error");
const manualRateStatus = document.querySelector("#manual-rate-status");
const staleWarning = document.querySelector("#stale-warning");

let manualRate = null;

function parsePtNumber(value) {
  const normalized = value.trim().replace(/\s/g, "").replace(/\.(?=\d{3}(?:\D|$))/g, "").replace(",", ".");
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatCurrency(value, currency) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency,
    maximumFractionDigits: currency === "JPY" || currency === "KRW" ? 0 : 2
  }).format(value);
}

function referenceRate(from, to) {
  return snapshot.rates[to] / snapshot.rates[from];
}

function track(event, details = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...details });
}

function syncManualLabels() {
  manualFrom.textContent = fromSelect.value;
  manualTo.textContent = toSelect.value;
  manualRateInput.placeholder = `Ex.: ${referenceRate(fromSelect.value, toSelect.value).toLocaleString("pt-BR", { maximumFractionDigits: 6 })}`;
}

function renderConversion({ reveal = false } = {}) {
  const amount = parsePtNumber(amountInput.value);
  const from = fromSelect.value;
  const to = toSelect.value;
  const rate = manualRate ?? referenceRate(from, to);
  if (amount <= 0) {
    amountError.textContent = "Informe um valor maior que zero.";
    amountInput.setAttribute("aria-invalid", "true");
    return false;
  }

  amountError.textContent = "";
  amountInput.removeAttribute("aria-invalid");
  const result = amount * rate;

  resultValue.textContent = formatCurrency(result, to);
  rateLine.textContent = `1 ${from} = ${rate.toLocaleString("pt-BR", { maximumFractionDigits: 6 })} ${to}${manualRate ? " · taxa manual" : ""}`;
  syncManualLabels();
  if (reveal) postConversion.hidden = false;
  return true;
}

Object.keys(snapshot.rates)
  .sort((a, b) => a.localeCompare(b))
  .forEach((code) => {
    const label = `${code} — ${currencyNames.of(code) ?? code}`;
    fromSelect.add(new Option(label, code));
    toSelect.add(new Option(label, code));
  });

fromSelect.value = "USD";
toSelect.value = "BRL";

document.querySelector("#converter-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (renderConversion({ reveal: true })) {
    track("calculation_completed", { from_currency: fromSelect.value, to_currency: toSelect.value, rate_mode: manualRate ? "manual" : "reference" });
  }
});

document.querySelector("#swap-currencies").addEventListener("click", () => {
  const currentFrom = fromSelect.value;
  fromSelect.value = toSelect.value;
  toSelect.value = currentFrom;
  manualRate = null;
  manualRateInput.value = "";
  if (postConversion.hidden) syncManualLabels();
  else renderConversion();
});

[fromSelect, toSelect].forEach((select) => {
  select.addEventListener("change", () => {
    manualRate = null;
    manualRateInput.value = "";
    if (postConversion.hidden) syncManualLabels();
    else renderConversion();
  });
});

document.querySelector("#apply-manual-rate").addEventListener("click", () => {
  const candidate = parsePtNumber(manualRateInput.value);
  manualRate = candidate > 0 ? candidate : null;
  manualRateStatus.textContent = manualRate ? "Taxa manual aplicada." : "Informe uma taxa maior que zero.";
  if (renderConversion({ reveal: true }) && manualRate) track("manual_rate_applied", { from_currency: fromSelect.value, to_currency: toSelect.value });
});

document.querySelector("#international-yes").addEventListener("click", () => {
  bridge.hidden = false;
  internationalArticleCard.hidden = false;
  bridge.scrollIntoView({ behavior: "smooth", block: "nearest" });
  track("international_context_selected", { answer: "yes" });
  track("cta_viewed", { destination: "credit_card" });
});

document.querySelector("#international-no").addEventListener("click", () => {
  bridge.hidden = true;
  internationalArticleCard.hidden = true;
  track("international_context_selected", { answer: "no" });
});

bridge.querySelector("a").addEventListener("click", () => {
  track("cta_clicked", { destination: "credit_card" });
});

document.querySelectorAll(".related-content-link").forEach((link) => {
  link.addEventListener("click", () => {
    track("related_content_clicked", {
      content_id: link.dataset.contentId,
      journey_stage: link.dataset.journeyStage
    });
  });
});

const snapshotAgeMs = Date.now() - new Date(`${snapshot.date}T12:00:00Z`).getTime();
if (snapshotAgeMs > 7 * 24 * 60 * 60 * 1000) staleWarning.hidden = false;

syncManualLabels();
