<?php
/*
 * Kalyani Boat Service: enquiry form handler for Hostinger.
 * Emails the enquiry to the business. Answers JSON to the page's script, or redirects when scripts are off.
 *
 * SETTINGS: $to receives the enquiries. $from must be an email address on this domain
 * (create it in Hostinger hPanel > Emails), otherwise many inboxes reject the message.
 */
$to   = 'alleppeyshikaratours@gmail.com';
$from = 'noreply@alleppeyshikaratours.com';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function finish($ok, $error = '')
{
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    } else {
        header('Location: ' . ($ok ? 'index.html?sent=1#book' : 'index.html?error=1#book'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: index.html', true, 303);
    exit;
}

$field = fn($k, $max = 200) => trim(mb_substr(str_replace(["\r", "\n"], ' ', (string)($_POST[$k] ?? '')), 0, $max));

// spam checks: the hidden "website" box must stay empty, and a person takes more than 3 seconds to fill the form
if ($field('website') !== '') finish(true);
$started = (int)$field('started') / 1000;
if ($started > 0 && time() - $started < 3) finish(true);

$tours = json_decode((string)@file_get_contents(__DIR__ . '/assets/js/tours.json'), true)['tours'] ?? [];
$tour = null;
foreach ($tours as $t) if ($t['slug'] === $field('tour')) $tour = $t;

$name    = $field('name', 80);
$phone   = $field('phone', 30);
$email   = $field('email', 120);
$date    = $field('date', 10);
$guests  = max(1, min(30, (int)$field('guests')));
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 1000));

if (!$tour) finish(false, 'Please choose a tour.');
if ($name === '' || !preg_match('/^[+0-9 ()-]{7,20}$/', $phone)) finish(false, 'Please enter your name and a valid phone number.');
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) finish(false, 'Please choose a date.');
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) finish(false, 'Please check your email address.');

$total = $tour['price'] + max(0, $guests - 2) * $tour['extra'] * $tour['hours'];
$body = "New enquiry from alleppeyshikaratours.com\n\n"
    . "Tour:    {$tour['name']} ({$tour['time']})\n"
    . "Date:    $date\n"
    . "Guests:  $guests\n"
    . "Price:   Rs " . number_format($total) . " (estimate shown on the website)\n\n"
    . "Name:    $name\n"
    . "Phone:   $phone\n"
    . "Email:   " . ($email ?: '-') . "\n\n"
    . "Note:\n" . ($message ?: '-') . "\n\n"
    . "WhatsApp the guest: https://wa.me/" . preg_replace('/\D/', '', $phone) . "\n";

$headers = [
    'From: Kalyani website <' . $from . '>',
    'Content-Type: text/plain; charset=UTF-8',
];
if ($email !== '') $headers[] = 'Reply-To: ' . $email;

$subject = '=?UTF-8?B?' . base64_encode("Enquiry: {$tour['name']}, $date, $guests guests") . '?=';
$sent = mail($to, $subject, $body, implode("\r\n", $headers), '-f' . $from);
finish($sent, 'Sorry, the enquiry could not be sent. Please use WhatsApp or call us.');
