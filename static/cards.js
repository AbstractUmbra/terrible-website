async function copyCardToClipboard(number) {
    let entry = document.getElementById(`card-${number}`);

    await navigator.clipboard.writeText(`TT Card #${number} - Pref healer, but can switch\nHelpers welcome too! Sync or helper boosted unsync works.`);
    document.querySelectorAll('.card-cb-button').forEach(btn => { btn.removeAttribute('disabled'); });

    entry.setAttribute("disabled", "disabled");
}
