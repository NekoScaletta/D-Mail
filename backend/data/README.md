# Dataset spam email

`spam.csv` currently uses the SpamAssassin email spam dataset referenced by OpenScience:

- OpenScience page: `https://openscience.vn/chi-tiet-du-lieu/bo-du-lieu-cac-thu-rac-email-176`
- Original source listed by OpenScience: `https://www.kaggle.com/datasets/nitishabharathi/email-spam-dataset`
- Download mirror used for automation: `https://huggingface.co/datasets/intelli-zen/spam_detect`

The training file is normalized to:

- `label`: `ham` or `spam`
- `text`: email body

`spam.sample_vi.csv` keeps the previous small Vietnamese demo dataset as a backup.
