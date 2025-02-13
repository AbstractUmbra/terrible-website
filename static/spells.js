async function copyToClipboard(number) {
    let entry = document.getElementById(`spell-${number}`);

    await navigator.clipboard.writeText(`BLU Spell #${number} - Pref healer, but can switch\nHelpers welcome too! Sync or helper boosted unsync works.`);
    document.querySelectorAll('.spell-cb-button').forEach(btn => { btn.removeAttribute('disabled'); });

    entry.setAttribute("disabled", "disabled");
}
