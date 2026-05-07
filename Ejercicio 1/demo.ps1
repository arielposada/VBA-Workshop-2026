Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Demo Suma Olimpo"
$form.Size = New-Object System.Drawing.Size(380,220)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

$lblA = New-Object System.Windows.Forms.Label
$lblA.Text = "A:"
$lblA.Location = New-Object System.Drawing.Point(30,30)
$lblA.AutoSize = $true

$txtA = New-Object System.Windows.Forms.TextBox
$txtA.Location = New-Object System.Drawing.Point(110,25)
$txtA.Size = New-Object System.Drawing.Size(180,27)

$lblB = New-Object System.Windows.Forms.Label
$lblB.Text = "B:"
$lblB.Location = New-Object System.Drawing.Point(30,70)
$lblB.AutoSize = $true

$txtB = New-Object System.Windows.Forms.TextBox
$txtB.Location = New-Object System.Drawing.Point(110,65)
$txtB.Size = New-Object System.Drawing.Size(180,27)

$btnSumar = New-Object System.Windows.Forms.Button
$btnSumar.Text = "Sumar"
$btnSumar.Location = New-Object System.Drawing.Point(110,105)
$btnSumar.Size = New-Object System.Drawing.Size(120,32)

$lblResultado = New-Object System.Windows.Forms.Label
$lblResultado.Text = "Resultado:"
$lblResultado.Location = New-Object System.Drawing.Point(30,155)
$lblResultado.AutoSize = $true

$btnSumar.Add_Click({
    try {
        $a = [double]::Parse($txtA.Text)
        $b = [double]::Parse($txtB.Text)
        $lblResultado.Text = "Resultado: " + ($a + $b)
    }
    catch {
        $lblResultado.Text = "Resultado: ERROR"
    }
})

$form.Controls.Add($lblA)
$form.Controls.Add($txtA)
$form.Controls.Add($lblB)
$form.Controls.Add($txtB)
$form.Controls.Add($btnSumar)
$form.Controls.Add($lblResultado)

[void]$form.ShowDialog()