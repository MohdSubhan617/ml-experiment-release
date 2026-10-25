# Operations and rollback

Validate changes in a clean environment before release. Keep the previous known-good version and artifact metadata. For a failed release, stop promotion and restore the previous pinned artifact/version; do not mutate an existing artifact in place. Inspect test logs and compare the exact commit before retrying.
