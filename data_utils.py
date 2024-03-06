def calculate_totals(data):
    total_dollars = 0.0
    total_pst = 0.0
    total_gst = 0.0

    for d in data:
        total_dollars += d['rate'] * d['qty']
        total_gst +=  (d['rate'] * d['qty']) * d['gst']
        total_pst +=  (d['rate'] * d['qty']) * d['pst']

    res = {
        'gst': '{:.2f}'.format(total_gst),
        'pst': '{:.2f}'.format(total_pst),
        'dollar': '{:.2f}'.format(total_dollars + total_gst + total_pst),
    }

    return res