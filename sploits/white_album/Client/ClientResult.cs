using System;
using Vostok.Clusterclient.Core.Model;

namespace DoNotIncludeThisPlease.Client
{
    public class ClientResult<T> : ClientResult
    {
        private readonly T result;

        public ClientResult(T result, bool isSuccessful, ResponseCode responseCode, string? error = null)
            : base(isSuccessful, responseCode, error)
        {
            this.result = result;
        }

        public T Result
        {
            get
            {
                EnsureSuccess();
                return result;
            }
        }
    }

    public class ClientResult
    {
        public ClientResult(bool isSuccessful, ResponseCode responseCode, string? error = null)
        {
            IsSuccessful = isSuccessful;
            ResponseCode = responseCode;
            Error = error;
        }

        public bool IsSuccessful { get; }

        public string? Error { get; }

        public ResponseCode ResponseCode { get; }

        public void EnsureSuccess()
        {
            if (IsSuccessful)
                return;
            
            var errorMessage = $"Request has failed with code = {ResponseCode}.";

            if (!string.IsNullOrWhiteSpace(Error))
                errorMessage += $" Server error = '{Error}'.";

            throw new Exception(errorMessage);
        }
    }
}