import 'dart:io';

import 'package:dio/dio.dart';
import 'package:miniclash/common/print.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('compactError compacts DioException to type and status code', () {
    final error = DioException(
      requestOptions: RequestOptions(path: '/'),
      type: DioExceptionType.badResponse,
      response: Response(
        requestOptions: RequestOptions(path: '/'),
        statusCode: 403,
      ),
    );
    expect(compactError(error), 'DioException(badResponse, HTTP 403)');
  });

  test('compactError omits the status code when the response is missing', () {
    final error = DioException(
      requestOptions: RequestOptions(path: '/'),
      type: DioExceptionType.connectionError,
    );
    expect(compactError(error), 'DioException(connectionError)');
  });

  test('compactError keeps the transport cause of a connection failure', () {
    final error = DioException(
      requestOptions: RequestOptions(path: '/'),
      type: DioExceptionType.connectionError,
      error: const SocketException('Connection refused'),
    );
    expect(
      compactError(error),
      'DioException(connectionError: SocketException: Connection refused)',
    );
  });

  test('compactError keeps other exception messages', () {
    expect(compactError(StateError('boom')), contains('boom'));
  });
}
