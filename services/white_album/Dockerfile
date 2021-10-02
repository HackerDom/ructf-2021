FROM mcr.microsoft.com/dotnet/sdk:5.0

COPY ./src /app

CMD ["bash", "-c", "export DOTNET_CLI_TELEMETRY_OPTOUT=1; cd /app && dotnet restore && dotnet publish -c Release -o publish"]


WORKDIR /app

ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 COMPlus_JitTelemetry=0 COMPlus_legacyCorruptedStateExceptionsPolicy=1 COMPlus_legacyUnhandledExceptionPolicy=1

RUN adduser --system --home /app --shell /usr/sbin/nologin --no-create-home --disabled-password deployer

CMD ["dotnet", "WhiteAlbum/bin/Debug/net5.0/WhiteAlbum.dll"]