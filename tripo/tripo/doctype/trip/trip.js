frappe.ui.form.on('Trip', {
    refresh(frm) {
        frm.trigger('generate_summary');
    },

    customer(frm) { frm.trigger('generate_summary'); },
    customer_name(frm) { frm.trigger('generate_summary'); },
    round_trip__one_way(frm) { frm.trigger('generate_summary'); },
    pickup_location(frm) { frm.trigger('generate_summary'); },
    destination(frm) { frm.trigger('generate_summary'); },
    trip_date(frm) { frm.trigger('generate_summary'); },
    trip_time(frm) { frm.trigger('generate_summary'); },
    trip_status(frm) { frm.trigger('generate_summary'); },
    trip_driver(frm) { frm.trigger('generate_summary'); },

    generate_summary(frm) {
    const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const day = String(date.getDate()).padStart(2, '0');
    const month = date.toLocaleString('en-GB', { month: 'short' });
    const year = date.getFullYear();
    const weekday = date.toLocaleString('en-GB', { weekday: 'long' });
    return `${day}-${month}-${year}, ${weekday}`;
};

    const formatTime = (timeStr) => {
        if (!timeStr) return '';
        const [hours, minutes] = timeStr.split(':');
        const date = new Date();
        date.setHours(+hours, +minutes);
        return date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }); // e.g., "5:30 PM"
    };

let summary_lines = [
    `Customer: ${frm.doc.customer_name || ''}`,
    `Pickup Location: ${frm.doc.pickup_location || ''}`,
    `Destination: ${frm.doc.destination || ''}`,
];

summary_lines.push(
    `Trip Date: ${formatDate(frm.doc.trip_date)}`,
    `Trip Time: ${formatTime(frm.doc.trip_time)}`,
    `Driver: ${frm.doc.trip_driver_name || ''}`
);

    let summary_text = summary_lines.join('\n');

frm.fields_dict.trip_summary.$wrapper.html(`
    <pre style="margin-bottom: 8px;" id="trip-summary-text">
${frappe.utils.escape_html(summary_text)}
</pre>
    <button class="btn btn-sm btn-primary" id="copy-summary-btn">📋 Copy Summary</button>
`);
    frm.fields_dict.trip_summary.$wrapper
        .find('#copy-summary-btn')
        .on('click', function () {
            const text = document.getElementById('trip-summary-text').innerText;
            navigator.clipboard.writeText(text).then(() => {
                frappe.show_alert('Summary copied to clipboard!');
            });
        });
}
});