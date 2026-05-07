Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Dunder Mifflin - Registro de Ventas"
$form.Size = New-Object System.Drawing.Size(520, 360)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

# Logo
$picLogo = New-Object System.Windows.Forms.PictureBox
$picLogo.Location = New-Object System.Drawing.Point(10, 10)
$picLogo.Size = New-Object System.Drawing.Size(80, 80)
$picLogo.SizeMode = "Zoom"

$logoPath = Join-Path $PSScriptRoot "Resources\logo.png"

if (Test-Path $logoPath) {
    $stream = [System.IO.File]::OpenRead($logoPath)
    $picLogo.Image = [System.Drawing.Image]::FromStream($stream)
    $stream.Close()
}

$form.Controls.Add($picLogo)

# 1. Vendedor
$lblVendedor = New-Object System.Windows.Forms.Label
$lblVendedor.Text = "Vendedor:"
$lblVendedor.Location = New-Object System.Drawing.Point(120, 30)
$lblVendedor.AutoSize = $true

$txtVendedor = New-Object System.Windows.Forms.TextBox
$txtVendedor.Location = New-Object System.Drawing.Point(280, 25)
$txtVendedor.Width = 180
$txtVendedor.TabIndex = 0

# 2. Fecha
$lblFecha = New-Object System.Windows.Forms.Label
$lblFecha.Text = "Fecha:"
$lblFecha.Location = New-Object System.Drawing.Point(120, 70)
$lblFecha.AutoSize = $true

$txtFecha = New-Object System.Windows.Forms.TextBox
$txtFecha.Location = New-Object System.Drawing.Point(280, 65)
$txtFecha.Width = 180
$txtFecha.TabIndex = 1

# 3. Cliente
$lblCliente = New-Object System.Windows.Forms.Label
$lblCliente.Text = "Cliente:"
$lblCliente.Location = New-Object System.Drawing.Point(120, 110)
$lblCliente.AutoSize = $true

$txtCliente = New-Object System.Windows.Forms.TextBox
$txtCliente.Location = New-Object System.Drawing.Point(280, 105)
$txtCliente.Width = 180
$txtCliente.TabIndex = 2

# 4. Cantidad papel vendido
$lblCantidadPapel = New-Object System.Windows.Forms.Label
$lblCantidadPapel.Text = "Cantidad de papel vendido:"
$lblCantidadPapel.Location = New-Object System.Drawing.Point(120, 150)
$lblCantidadPapel.AutoSize = $true

$txtCantidadPapel = New-Object System.Windows.Forms.TextBox
$txtCantidadPapel.Location = New-Object System.Drawing.Point(280, 145)
$txtCantidadPapel.Width = 180
$txtCantidadPapel.TabIndex = 3

# Botón
$btnRegistrar = New-Object System.Windows.Forms.Button
$btnRegistrar.Text = "Registrar venta"
$btnRegistrar.Location = New-Object System.Drawing.Point(280, 190)
$btnRegistrar.Width = 140
$btnRegistrar.TabIndex = 4

# Resultado
$lblResultado = New-Object System.Windows.Forms.Label
$lblResultado.Text = "Resultado:"
$lblResultado.Location = New-Object System.Drawing.Point(120, 250)
$lblResultado.AutoSize = $true
$lblResultado.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)

function Escape-CsvValue {
    param(
        [string]$Value
    )

    if ($null -eq $Value) {
        return ""
    }

    if ($Value.Contains(",") -or $Value.Contains('"') -or $Value.Contains("`n") -or $Value.Contains("`r")) {
        $Value = $Value.Replace('"', '""')
        return '"' + $Value + '"'
    }

    return $Value
}

$btnRegistrar.Add_Click({
    $vendedor = $txtVendedor.Text.Trim()
    $fecha = $txtFecha.Text.Trim()
    $cliente = $txtCliente.Text.Trim()
    $cantidadTexto = $txtCantidadPapel.Text.Trim()

    if ([string]::IsNullOrWhiteSpace($vendedor) -or
        [string]::IsNullOrWhiteSpace($fecha) -or
        [string]::IsNullOrWhiteSpace($cliente) -or
        [string]::IsNullOrWhiteSpace($cantidadTexto)) {

        $lblResultado.Text = "Resultado: FALTAN DATOS"
        return
    }

    $cantidad = 0.0
    $ok = [double]::TryParse(
        $cantidadTexto,
        [System.Globalization.NumberStyles]::Any,
        [System.Globalization.CultureInfo]::InvariantCulture,
        [ref]$cantidad
    )

    if (-not $ok) {
        $lblResultado.Text = "Resultado: CANTIDAD INVALIDA"
        return
    }

    try {
        $folderPath = "C:\Temp"
        $filePath = Join-Path $folderPath "Registro.csv"

        if (-not (Test-Path $folderPath)) {
            New-Item -Path $folderPath -ItemType Directory | Out-Null
        }

        $fileExists = Test-Path $filePath

        if (-not $fileExists) {
            "Vendedor,Fecha,Cliente,CantidadPapel" | Out-File -FilePath $filePath -Encoding UTF8
        }

        $csvLine = "$(Escape-CsvValue $vendedor),$(Escape-CsvValue $fecha),$(Escape-CsvValue $cliente),$($cantidad.ToString([System.Globalization.CultureInfo]::InvariantCulture))"

        Add-Content -Path $filePath -Value $csvLine -Encoding UTF8

        $lblResultado.Text = "Resultado: Venta registrada y guardada en CSV"
    }
    catch {
        $lblResultado.Text = "Resultado: ERROR AL GUARDAR"
        [System.Windows.Forms.MessageBox]::Show(
            "No se pudo guardar el registro:`n$($_.Exception.Message)",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    }
})

$form.Controls.Add($lblVendedor)
$form.Controls.Add($txtVendedor)

$form.Controls.Add($lblFecha)
$form.Controls.Add($txtFecha)

$form.Controls.Add($lblCliente)
$form.Controls.Add($txtCliente)

$form.Controls.Add($lblCantidadPapel)
$form.Controls.Add($txtCantidadPapel)

$form.Controls.Add($btnRegistrar)
$form.Controls.Add($lblResultado)

[void]$form.ShowDialog()