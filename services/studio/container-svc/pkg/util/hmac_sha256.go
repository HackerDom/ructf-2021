package util

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
)

func EncodeSha256(value string) string {
	sig := hmac.New(sha256.New, []byte("SUPERSECRET_KEY"))
	sig.Write([]byte(value))
	return hex.EncodeToString(sig.Sum(nil))
}
