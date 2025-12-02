async function copyBeastToClipboard(number) {
    let entry = document.getElementById(`beast-${number}`);

    await navigator.clipboard.writeText(`Beast tame #${number} - Pref healer, but can switch\nHelpers welcome too! Sync or helper boosted unsync works.`);
    document.querySelectorAll('.beast-cb-button').forEach(btn => { btn.removeAttribute('disabled'); });

    entry.setAttribute("disabled", "disabled");
}
