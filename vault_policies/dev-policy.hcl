path "secret/*" {
  policy = "read"
}

path "auth/*" {
  policy = "deny"
}

path "sys/*" {
  policy = "deny"
}
