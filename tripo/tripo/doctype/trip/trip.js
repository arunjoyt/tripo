frappe.ui.form.on('Trip', {
    refresh(frm) {
        frm.trigger('generate_summary');
    },

    customer(frm) { frm.trigger('generate_summary'); },
    customer_name(frm) { frm.trigger('generate_summary'); },
    customer_phone(frm) { frm.trigger('generate_summary'); },
    customer_address(frm) { frm.trigger('generate_summary'); },
    round_trip__one_way(frm) { frm.trigger('generate_summary'); },
    pickup_location(frm) { frm.trigger('generate_summary'); },
    google_maps_location_pickup(frm) { frm.trigger('generate_summary'); },
    destination(frm) { frm.trigger('generate_summary'); },
    google_maps_location_destination(frm) { frm.trigger('generate_summary'); },
    trip_date(frm) { frm.trigger('generate_summary'); },
    trip_time(frm) { frm.trigger('generate_summary'); },
    trip_date_and_time(frm) { frm.trigger('generate_summary'); },
    trip_status(frm) { frm.trigger('generate_summary'); },
    trip_driver(frm) { frm.trigger('generate_summary'); },
    trip_driver_name(frm) { frm.trigger('generate_summary'); },
    

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
            `Phone: ${frm.doc.customer_phone || ''}`,
            `${frm.doc.round_trip__one_way|| ''}`,
            `Pickup Location: ${frm.doc.pickup_location || ''}`,
            `${frm.doc.google_maps_location_pickup || ''}`,
            `Destination: ${frm.doc.destination || ''}`,
            `${frm.doc.google_maps_location_destination || ''}`,
            `Trip Date: ${formatDate(frm.doc.trip_date)}`,
            `Trip Time: ${frm.doc.trip_time}`,
            `Trip Status: ${frm.doc.trip_status}`,
            `Driver: ${frm.doc.trip_driver_name || ''}`,
            `Driver Phone: ${frm.doc.driver_phone_1 || ''}`
        ];

        let summary_text = summary_lines.join('\n');

        frm.fields_dict.trip_summary.$wrapper.html(`
            <pre style="margin-bottom: 8px;" id="trip-summary-text">${frappe.utils.escape_html(summary_text)}</pre>
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
    },

    // Time entry in 12H(AM/PM) format
    trip_time(frm) {
        const input = frm.doc.trip_time?.trim();
        if (!input) {
            frm.set_value('trip_date_and_time', '');
            return;
        }

        const regex = /^(0?[1-9]|1[0-2]):([0-5][0-9])\s?(AM|PM)$/i;
        const match = input.match(regex);

        if (!match) {
            // Show alert only if user typed 7+ characters
            if (input.length >= 7) {
                frappe.show_alert({
                    message: __('Invalid time. Use format: hh:mm AM/PM (e.g., 9:45 PM)'),
                    indicator: 'orange'
                });
            }
            frm.set_value('trip_date_and_time', '');
            return;
        }

        let [_, hourStr, minute, ampm] = match;
        let hour = parseInt(hourStr, 10);
        ampm = ampm.toUpperCase();

        if (ampm === 'PM' && hour !== 12) hour += 12;
        if (ampm === 'AM' && hour === 12) hour = 0;

        const datePart = frm.doc.trip_date;
        if (!datePart) {
            frappe.show_alert({
                message: __('Please set the Trip Date before entering time.'),
                indicator: 'orange'
            });
            return;
        }

        // Build a datetime string: yyyy-mm-dd HH:MM:00
        const time24 = `${String(hour).padStart(2, '0')}:${minute}:00`;
        const datetime = `${datePart} ${time24}`;

        frm.set_value('trip_date_and_time', datetime);
    },

    validate(frm) {
        const input = frm.doc.trip_time?.trim();
        if (!input) return;

        const regex = /^(0?[1-9]|1[0-2]):([0-5][0-9])\s?(AM|PM)$/i;
        if (!regex.test(input)) {
            frappe.throw(__('Invalid time format in "Trip Time". Use hh:mm AM/PM (e.g., 10:30 PM)'));
        }
    }
});