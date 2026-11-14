"""Ek sayfalar (v2.2): Destek rehberi (B), Trend ve ortam analizi (D), Gizlilik ve KVKK paneli (E)."""
from __future__ import annotations

import html

import streamlit as st

import db
from sabitler import ACIL_HATLAR, OLAY_TURLERI, ORTAMLAR

ss = st.session_state


def _acil() -> None:
    parca = " · ".join(f"<b>{html.escape(n)}</b> {html.escape(a)}" for n, a in ACIL_HATLAR)
    st.markdown(f"<div class='emergency'>Acil bir tehlike varsa beklemeyin: {parca}</div>", unsafe_allow_html=True)


def _baslik(ust: str, baslik: str, aciklama: str) -> None:
    st.markdown(f"<div class='page-heading'><div class='eyebrow-dark'>{html.escape(ust)}</div>"
                f"<h1>{html.escape(baslik)}</h1><p>{html.escape(aciklama)}</p></div>", unsafe_allow_html=True)


ICERIK = {
    "Öğrenciler": (
        ("Zorbalık nedir, ne değildir?", ("Zorbalık; bilerek yapılan, tekrar eden ve güç dengesizliği olan davranıştır.", "Tek seferlik tartışma genellikle zorbalık sayılmaz.")),
        ("Yaşıyorsan ne yapabilirsin?", ("Güvendiğin bir yetişkine anlat.", "Mesaj ve ekran görüntülerini sakla.", "Anonim formu kullanabilirsin.")),
    ),
    "Tanık olanlar": (
        ("Gördüysen sessiz kalma", ("Zorbalığa gülmek ya da paylaşmak onu büyütür.", "Güvenliysen mağdurun yanına git.")),
    ),
    "Siber zorbalık": (
        ("İnternette aşağılanıyor ya da tehdit ediliyorsan", ("Cevap verme, kişiyi engelle.", "Kanıtları sakla.", "Yetişkine haber ver.")),
    ),
    "Veliler": (
        ("Çocuğunuz zorbalığa uğruyor olabilir", ("Sık görülen işaretler: okula gitmek istememe, uyku/iştah değişikliği.", "Sakin kalın, dinleyin.")),
    ),
    "Öğretmenler": (
        ("Bildirim geldiğinde", ("Kaydı insan olarak değerlendirin.", "Acil sinyal varsa okul protokolünü uygulayın.")),
    ),
}

AKIS = (
    "Formu gönderirsin ve gizli takip kodunu alırsın.",
    "Kayıt, yetkili kişiler tarafından incelenir; bunu bir insan yapar.",
    "Takip koduyla durumu görürsün. Acil durumlarda yetişkine ulaş.")


def destek() -> None:
    _baslik("DESTEK", "Destek rehberi", "Zorbalıkla baş etme yolları ve nasıl destek alabileceğin.")
    _acil()
    sekmeler = st.tabs(list(ICERIK) + ["Bildirimden sonra ne olur?"])
    for sekme, (ad, bolumler) in zip(sekmeler, ICERIK.items()):
        with sekme:
            for baslik, maddeler in bolumler:
                with st.expander(baslik, expanded=baslik == bolumler[0][0]):
                    st.markdown("\n".join(f"- {m}" for m in maddeler))
    with sekmeler[-1]:
        st.markdown("\n".join(f"{i}. {a}" for i, a in enumerate(AKIS, 1)))


def _isi_tablosu(matris: dict, satirlar: list[str], sutunlar: list[str]) -> str:
    en_buyuk = max(matris.values(), default=1)
    bas = "".join(f"<th style='padding:.4rem;font-size:.75rem'>{html.escape(c)}</th>" for c in sutunlar)
    govde = []
    for r in satirlar:
        hucre = []
        for c in sutunlar:
            v = matris.get((r, c))
            if v is None:
                hucre.append("<td style='text-align:center;color:#9aa8b8'>·</td>")
            else:
                a = 0.15 + 0.75 * v / en_buyuk
                hucre.append(f"<td style='text-align:center;font-weight:700;background:rgba(49,95,150,{a:.2f});color:{'#fff' if a > .55 else '#1d2b3d'}'>{v}</td>")
        govde.append(f"<tr><th style='text-align:left;padding:.4rem;font-size:.8rem'>{html.escape(r)}</th>" + "".join(hucre) + "</tr>")
    return "<div style='overflow-x:auto'><table style='border-collapse:collapse;width:100%'><tr><th></th>" + bas + "</tr>" + "".join(govde) + "</table></div>"


def trend() -> None:
    _baslik("ANALİTİK", "Trend ve ortam analizi", "Bildirimlerin saat, gün ve mekân dağılımı.")
    c1, c2 = st.columns(2)
    gun = c1.selectbox("Dönem", [30, 90, 180, 365], index=1, format_func=lambda g: f"Son {g} gün", key="trend_gun")
    k = c2.number_input("Küçük hücre eşiği (k)", min_value=3, max_value=20, value=5, key="trend_k")
    o = db.trend_ozeti(int(gun), int(k))
    if not o["toplam"]:
        st.info("Bu dönemde kayıt yok.")
        return
    if o["toplam"] < 20:
        st.warning(f"Yalnızca {o['toplam']} kayıt var; yorum yapmayın.")
    m = st.columns(3)
    m[0].metric("Kayıt sayısı", o["toplam"])
    en_cok_ortam = next(iter(o["ortam"]), "—")
    m[1].metric("En çok bildirilen ortam", en_cok_ortam)
    m[2].metric("En çok bildirilen tür", next(iter(o["tur"]), "—"))

    st.subheader("Ne zaman bildiriliyor?")
    a, b = st.columns(2, gap="large")
    with a:
        st.caption("Saate göre")
        st.bar_chart({f"{h:02d}": v for h, v in o["saat"].items()})
    with b:
        st.caption("Haftanın gününe göre")
        st.bar_chart(o["haftanin_gunu"])
    st.subheader("Haftalık eğilim")
    st.bar_chart(o["hafta"])
    st.subheader("Hangi ortamda, hangi tür?")
    d1, d2 = st.columns(2, gap="large")
    with d1:
        st.caption("Ortama göre")
        st.bar_chart(o["ortam"], horizontal=True)
    with d2:
        st.caption("Olay türüne göre")
        st.bar_chart(o["tur"], horizontal=True)
    st.markdown("**Ortam haritası (ısı tablosu)**")
    st.markdown(_isi_tablosu(o["matris"], ORTAMLAR, [t for t in OLAY_TURLERI]), unsafe_allow_html=True)


AYDINLATMA = """**Veri sorumlusu:** [OKUL ADI / KURUM] · **İletişim:** [KVKK İLETİŞİM ADRESİ]\n\n**İşlenen veriler:** Bildirim formunda yazdığınız olay bilgisi.\n\n**Amaç:** Akran zorbalığı bildirimlerinin incelenmesi ve öğrencinin korunması.\n\n**Haklarınız:** KVKK m.11 kapsamındaki haklar için yukarıdaki adrese başvurabilirsiniz."""

ENVANTER = (
    ("Olay açıklaması (maskelenmiş)", "Bildirimi incelemek", "Bildirim gönderildiğinde", "Sonuç + [180] gün", "Serbest metin; üçüncü kişilerin adı geçebilir."),
    ("Olay türü, ortam, zaman, tekrar", "İstatistik ve önceliklendirme", "Bildirim gönderildiğinde", "Sonuç + [180] gün", "Seçmeli alanlar."),
)


def kvkk(yonetici: bool) -> None:
    _baslik("GİZLİLİK", "Gizlilik ve KVKK paneli", "Hangi veri neden toplanıyor, ne kadar saklanıyor ve nasıl siliniyor.")
    s1, s2, s3 = st.tabs(["Aydınlatma metni", "Veri envanteri", "Saklama ve imha"])
    with s1:
        st.markdown(AYDINLATMA)
    with s2:
        st.dataframe([dict(zip(("Veri", "Amaç", "Ne zaman", "Saklama", "Not"), r)) for r in ENVANTER], hide_index=True)
    with s3:
        st.markdown("- Sonuçlanan kayıtlar kanunen belirli süre sonra silinir.\n- Cihaz jetonu özeti 1 gün sonra silinir.")
